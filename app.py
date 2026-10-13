import streamlit as st
import time
import json
from datetime import datetime
from questoes import PRIMEIRA_FASE, SEGUNDA_FASE
from esconder_selo import esconder_selo_streamlit

# ─── Configuração da página ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Simulador FUVEST 2025",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)
esconder_selo_streamlit()  # oculta os controles do Streamlit Cloud

# ─── CSS Personalizado ────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600;700&display=swap');

    :root {
        --azul-fuvest: #003082;
        --azul-medio: #0050B3;
        --azul-claro: #E8F0FE;
        --dourado: #C8962A;
        --dourado-claro: #FFF3CD;
        --verde: #1B7F3B;
        --verde-claro: #D4EDDA;
        --vermelho: #B71C1C;
        --vermelho-claro: #FFEBEE;
        --cinza: #F5F6FA;
        --cinza-borda: #DEE2E6;
        --texto: #000000;
        --texto-suave: #6B7280;
    }

    html, body, .stApp {
        font-family: 'Source Sans 3', sans-serif;
        background-color: #F0F2F8;
        color: #000000 !important;
    }

    /* Força preto em TODO texto da área principal */
    .main .block-container p,
    .main .block-container div,
    .main .block-container span,
    .main .block-container li,
    .stMarkdown p,
    .stMarkdown div,
    .stMarkdown span,
    .element-container p,
    .element-container div,
    .element-container span {
        color: #000000 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--azul-fuvest) 0%, #001A4D 100%);
        color: white;
    }
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stRadio label {
        color: #CBD5E0 !important;
        font-size: 0.85rem !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        background: var(--dourado) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
        transition: all 0.2s !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background: #A07820 !important;
        transform: translateY(-1px) !important;
    }

    /* Header principal */
    .fuvest-header {
        background: linear-gradient(135deg, var(--azul-fuvest) 0%, var(--azul-medio) 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 1.5rem;
        color: white;
        position: relative;
        overflow: hidden;
    }
    .fuvest-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -10%;
        width: 300px;
        height: 300px;
        background: rgba(255,255,255,0.05);
        border-radius: 50%;
    }
    .fuvest-header h1 {
        font-family: 'Playfair Display', serif;
        font-size: 2.2rem;
        font-weight: 900;
        margin: 0;
        color: white;
    }
    .fuvest-header p {
        color: #A8C4FF;
        margin: 0.3rem 0 0;
        font-size: 1rem;
    }
    .fuvest-badge {
        display: inline-block;
        background: var(--dourado);
        color: white;
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    /* Cards de questão */
    .questao-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border-left: 4px solid var(--azul-fuvest);
        transition: box-shadow 0.2s;
    }
    .questao-card:hover {
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    }
    .questao-numero {
        font-family: 'Playfair Display', serif;
        font-size: 0.85rem;
        color: var(--azul-medio);
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .area-badge {
        display: inline-block;
        background: var(--azul-claro);
        color: var(--azul-fuvest);
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Alternativas */
    div[data-testid="stRadio"] > label {
        display: none !important;
    }
    div[data-testid="stRadio"] > div {
        gap: 0.5rem !important;
        display: flex !important;
        flex-direction: column !important;
    }
    div[data-testid="stRadio"] > div > label {
        background: var(--cinza);
        border: 2px solid var(--cinza-borda);
        border-radius: 10px;
        padding: 0.8rem 1.2rem !important;
        transition: all 0.2s;
        cursor: pointer;
    }
    div[data-testid="stRadio"] > div > label p,
    div[data-testid="stRadio"] > div > label span,
    div[data-testid="stRadio"] > div > label div {
        color: #000000 !important;
    }
    div[data-testid="stRadio"] > div > label:hover {
        border-color: var(--azul-medio);
        background: var(--azul-claro);
    }
    div[data-testid="stRadio"] > div > label[data-checked="true"] {
        border-color: var(--azul-fuvest);
        background: var(--azul-claro);
    }

    /* Botões principais */
    .stButton > button {
        background: linear-gradient(135deg, var(--azul-fuvest), var(--azul-medio));
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(0,48,130,0.3);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,48,130,0.4);
    }

    /* Resultado boxes */
    .resultado-correto {
        background: var(--verde-claro);
        border: 2px solid var(--verde);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        color: #000000 !important;
    }
    .resultado-correto * { color: #000000 !important; }
    .resultado-errado {
        background: var(--vermelho-claro);
        border: 2px solid var(--vermelho);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin: 0.5rem 0;
        color: #000000 !important;
    }
    .resultado-errado * { color: #000000 !important; }
    .explicacao-box {
        background: var(--dourado-claro);
        border-left: 4px solid var(--dourado);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin-top: 0.5rem;
        color: #000000 !important;
    }
    .explicacao-box * { color: #000000 !important; }

    /* Placar/Stats */
    .stat-card {
        background: white;
        border-radius: 14px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border-top: 3px solid var(--azul-fuvest);
    }
    .stat-numero {
        font-family: 'Playfair Display', serif;
        font-size: 2.5rem;
        font-weight: 900;
        color: var(--azul-fuvest);
        line-height: 1;
    }
    .stat-label {
        color: var(--texto-suave);
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.3rem;
    }

    /* Timer */
    .timer-box {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border: 2px solid var(--cinza-borda);
        margin-bottom: 1rem;
    }
    .timer-text {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--azul-fuvest);
    }

    /* Gabarito 2ª fase */
    .gabarito-box {
        background: #F0FFF4;
        border: 2px solid var(--verde);
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1rem;
    }

    /* Progresso */
    .progresso-info {
        display: flex;
        justify-content: space-between;
        color: var(--texto-suave);
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }

    /* Navegação de questões */
    .nav-questoes {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin: 1rem 0;
    }

    /* Texto de questão */
    .enunciado-texto {
        font-size: 1rem;
        line-height: 1.7;
        color: #000000 !important;
    }
    .enunciado-texto * {
        color: #000000 !important;
    }
    /* Força preto em todo texto do conteúdo principal */
    .main p, .main div, .main span, .main li {
        color: #000000 !important;
    }

    /* Separador decorativo */
    .separator {
        height: 3px;
        background: linear-gradient(90deg, var(--azul-fuvest), var(--azul-claro));
        border-radius: 3px;
        margin: 1.5rem 0;
    }

    /* Score final */
    .score-final {
        background: linear-gradient(135deg, var(--azul-fuvest), var(--azul-medio));
        color: white;
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 8px 30px rgba(0,48,130,0.3);
    }
    .score-nota {
        font-family: 'Playfair Display', serif;
        font-size: 5rem;
        font-weight: 900;
        line-height: 1;
    }

    /* Textarea 2a fase */
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 2px solid var(--cinza-borda) !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        padding: 1rem !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: var(--azul-medio) !important;
    }

    /* Remove padrão streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem;
        max-width: 900px;
    }
</style>
""", unsafe_allow_html=True)

# ─── Inicialização do estado ───────────────────────────────────────────────────
def init_state():
    defaults = {
        "fase": None,
        "modo": "simulado",
        "questao_atual": 0,
        "respostas": {},
        "respondidas": set(),
        "gabarito_exibido": set(),
        "inicio": None,
        "finalizado": False,
        "segunda_respostas": {},
        "gabarito_2f_visivel": set(),
        "filtro_area": "Todas",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ─── Funções auxiliares ────────────────────────────────────────────────────────
def tempo_decorrido():
    if st.session_state.inicio:
        delta = datetime.now() - st.session_state.inicio
        h = int(delta.total_seconds() // 3600)
        m = int((delta.total_seconds() % 3600) // 60)
        s = int(delta.total_seconds() % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
    return "00:00:00"

def calcular_resultados():
    corretas = 0
    total = len(PRIMEIRA_FASE)
    por_area = {}
    for q in PRIMEIRA_FASE:
        area = q["area"]
        if area not in por_area:
            por_area[area] = {"corretas": 0, "total": 0}
        por_area[area]["total"] += 1
        resp = st.session_state.respostas.get(q["id"])
        if resp == q["resposta"]:
            corretas += 1
            por_area[area]["corretas"] += 1
    return corretas, total, por_area

def resetar_simulado():
    st.session_state.fase = None
    st.session_state.questao_atual = 0
    st.session_state.respostas = {}
    st.session_state.respondidas = set()
    st.session_state.gabarito_exibido = set()
    st.session_state.inicio = None
    st.session_state.finalizado = False
    st.session_state.segunda_respostas = {}
    st.session_state.gabarito_2f_visivel = set()

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0 1.5rem;'>
        <div style='font-size:3rem;'>🎓</div>
        <div style='font-family: Playfair Display, serif; font-size:1.4rem; font-weight:900; color:white;'>FUVEST</div>
        <div style='color: #90CAF9; font-size:0.85rem; letter-spacing:2px;'>SIMULADOR 2025</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Menu principal
    st.markdown("<p style='color:#90CAF9; font-size:0.8rem; letter-spacing:1px; text-transform:uppercase;'>Navegação</p>", unsafe_allow_html=True)

    if st.button("🏠 Início", use_container_width=True):
        resetar_simulado()
        st.rerun()

    if st.session_state.fase:
        if st.button("🔄 Reiniciar Simulado", use_container_width=True):
            resetar_simulado()
            st.rerun()

    st.markdown("---")

    # Info
    if st.session_state.fase == "1a" and st.session_state.inicio and not st.session_state.finalizado:
        st.markdown(f"""
        <div class='timer-box' style='background:rgba(255,255,255,0.1); border-color:rgba(255,255,255,0.2);'>
            <div style='color:#90CAF9; font-size:0.75rem; text-transform:uppercase;'>⏱️ Tempo</div>
            <div class='timer-text' style='color:white; font-size:1.4rem;'>{tempo_decorrido()}</div>
        </div>
        """, unsafe_allow_html=True)

        respondidas = len(st.session_state.respondidas)
        total = len(PRIMEIRA_FASE)
        st.markdown(f"""
        <div style='color:#90CAF9; font-size:0.85rem;'>Progresso: {respondidas}/{total} questões</div>
        """, unsafe_allow_html=True)
        st.progress(respondidas / total)

    if st.session_state.fase == "1a" and st.session_state.inicio:
        st.markdown("---")
        st.markdown("<p style='color:#90CAF9; font-size:0.8rem; letter-spacing:1px; text-transform:uppercase;'>Filtrar por Área</p>", unsafe_allow_html=True)
        areas = ["Todas"] + sorted(list(set(q["area"] for q in PRIMEIRA_FASE)))
        filtro = st.selectbox("", areas, label_visibility="collapsed")
        st.session_state.filtro_area = filtro

    st.markdown("---")
    st.markdown("""
    <div style='color:#6B8CC7; font-size:0.75rem; text-align:center; padding:0.5rem;'>
        Simulador não oficial.<br>
        Conteúdo baseado no estilo<br>FUVEST 2025.
    </div>
    """, unsafe_allow_html=True)

# ─── TELA INICIAL ─────────────────────────────────────────────────────────────
if st.session_state.fase is None:
    st.markdown("""
    <div class='fuvest-header'>
        <h1>🎓 Simulador FUVEST 2025</h1>
        <p>Prepare-se para o vestibular mais concorrido do Brasil</p>
    </div>
    """, unsafe_allow_html=True)

    # Stats gerais
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""<div class='stat-card'>
            <div class='stat-numero'>40</div>
            <div class='stat-label'>Questões 1ª Fase</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class='stat-card'>
            <div class='stat-numero'>8</div>
            <div class='stat-label'>Questões 2ª Fase</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class='stat-card'>
            <div class='stat-numero'>10</div>
            <div class='stat-label'>Disciplinas</div>
        </div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class='stat-card'>
            <div class='stat-numero'>5h</div>
            <div class='stat-label'>Tempo Real</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

    # Escolha da fase
    st.markdown("<h3 style='color:#000000; font-family: Source Sans 3, sans-serif; font-weight:700; margin-bottom:1rem;'>Escolha o Simulado</h3>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div style='background:white; border-radius:16px; padding:2rem; box-shadow:0 2px 12px rgba(0,0,0,0.08); border-top:4px solid #003082;'>
            <div style='font-size:2.5rem; margin-bottom:0.5rem;'>📝</div>
            <h3 style='color:#003082; font-family: Playfair Display, serif; margin:0 0 0.5rem;'>Primeira Fase</h3>
            <p style='color:#6B7280; font-size:0.9rem; line-height:1.6;'>
                <strong>40 questões</strong> de múltipla escolha<br>
                Cobrindo Português, Matemática, Ciências da Natureza, Ciências Humanas e Inglês<br>
                Gabarito imediato e explicações detalhadas
            </p>
            <div style='font-size:0.8rem; color:#003082; font-weight:600; margin-top:0.5rem;'>⏱️ Duração estimada: 3h</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        modo = st.radio(
            "Modo de estudo:",
            ["🏆 Simulado (sem gabarito durante)", "📚 Estudo (gabarito imediato)"],
            key="modo_1f"
        )

    with col_b:
        st.markdown("""
        <div style='background:white; border-radius:16px; padding:2rem; box-shadow:0 2px 12px rgba(0,0,0,0.08); border-top:4px solid #C8962A;'>
            <div style='font-size:2.5rem; margin-bottom:0.5rem;'>✍️</div>
            <h3 style='color:#C8962A; font-family: Playfair Display, serif; margin:0 0 0.5rem;'>Segunda Fase</h3>
            <p style='color:#6B7280; font-size:0.9rem; line-height:1.6;'>
                <strong>8 questões dissertativas</strong><br>
                Português, Matemática, Física, Química, Biologia, História/Geografia e Redação<br>
                Com gabarito modelo para autoavaliação
            </p>
            <div style='font-size:0.8rem; color:#C8962A; font-weight:600; margin-top:0.5rem;'>⏱️ Duração estimada: 5h</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)

        # Espaço equivalente ao radio da col_a para alinhar os botões
        st.markdown("<div style='height:4.6rem'></div>", unsafe_allow_html=True)

    # Botões na mesma linha, fora dos withs — garantindo alinhamento perfeito
    col_btn_a, col_btn_b = st.columns(2)
    with col_btn_a:
        if st.button("▶ Iniciar 1ª Fase", use_container_width=True, key="btn_1f"):
            st.session_state.fase = "1a"
            st.session_state.modo = "simulado" if "Simulado" in modo else "estudo"
            st.session_state.inicio = datetime.now()
            st.session_state.questao_atual = 0
            st.rerun()
    with col_btn_b:
        if st.button("▶ Iniciar 2ª Fase", use_container_width=True, key="btn_2f"):
            st.session_state.fase = "2a"
            st.session_state.inicio = datetime.now()
            st.session_state.questao_atual = 0
            st.rerun()

# ─── PRIMEIRA FASE ────────────────────────────────────────────────────────────
elif st.session_state.fase == "1a" and not st.session_state.finalizado:

    # Filtrar questões por área
    questoes = PRIMEIRA_FASE
    if st.session_state.filtro_area != "Todas":
        questoes = [q for q in PRIMEIRA_FASE if q["area"] == st.session_state.filtro_area]

    if not questoes:
        st.warning("Nenhuma questão encontrada para essa área.")
        st.stop()

    # Header
    respondidas = len(st.session_state.respondidas)
    total = len(PRIMEIRA_FASE)
    st.markdown(f"""
    <div class='fuvest-header'>
        <div class='fuvest-badge'>1ª Fase • {st.session_state.modo.upper()}</div>
        <h1>Primeira Fase</h1>
        <p>{respondidas}/{total} questões respondidas • {len(questoes)} questões {('— ' + st.session_state.filtro_area) if st.session_state.filtro_area != 'Todas' else ''}</p>
    </div>
    """, unsafe_allow_html=True)

    # Navegação por questão atual
    idx = min(st.session_state.questao_atual, len(questoes) - 1)
    q = questoes[idx]

    # Navegação
    col_nav_prev, col_nav_info, col_nav_next = st.columns([1, 3, 1])
    with col_nav_prev:
        if idx > 0:
            if st.button("◀ Anterior"):
                st.session_state.questao_atual = idx - 1
                st.rerun()
    with col_nav_info:
        st.markdown(f"""
        <div style='text-align:center; padding:0.5rem; color:#6B7280; font-size:0.9rem;'>
            Questão <strong>{idx+1}</strong> de <strong>{len(questoes)}</strong>
        </div>
        """, unsafe_allow_html=True)
    with col_nav_next:
        if idx < len(questoes) - 1:
            if st.button("Próxima ▶"):
                st.session_state.questao_atual = idx + 1
                st.rerun()

    # Card da questão
    status_icon = "✅" if q["id"] in st.session_state.respondidas else "⬜"
    enunciado_html = q["enunciado"].replace("\n", "<br>")
    st.markdown(f"""
    <div class='questao-card'>
        <div class='questao-numero'>{status_icon} Questão {q['id']}</div>
        <div class='area-badge'>📚 {q['area']}</div>
        <div class='enunciado-texto' style='color:#000000 !important;'>
            {enunciado_html}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Alternativas
    resp_atual = st.session_state.respostas.get(q["id"])
    alternativas_lista = [f"**{k})** {v}" for k, v in q["alternativas"].items()]
    alternativas_keys = list(q["alternativas"].keys())

    idx_sel = alternativas_keys.index(resp_atual) if resp_atual in alternativas_keys else None

    col_q, col_esp = st.columns([3, 1])
    with col_q:
        escolha = st.radio(
            "Selecione sua resposta:",
            alternativas_lista,
            index=idx_sel,
            key=f"radio_{q['id']}"
        )

        if escolha:
            letra = alternativas_lista.index(escolha)
            st.session_state.respostas[q["id"]] = alternativas_keys[letra]
            st.session_state.respondidas.add(q["id"])

    # Botão confirmar / ver gabarito
    col_btn1, col_btn2, col_btn3 = st.columns([2, 2, 3])
    with col_btn1:
        if st.button("✅ Confirmar Resposta", use_container_width=True):
            st.session_state.gabarito_exibido.add(q["id"])
            st.rerun()

    with col_btn2:
        if st.session_state.modo == "estudo":
            if st.button("📖 Ver Gabarito", use_container_width=True):
                st.session_state.gabarito_exibido.add(q["id"])

    # Exibir resultado
    if q["id"] in st.session_state.gabarito_exibido:
        resp_user = st.session_state.respostas.get(q["id"])
        gabarito = q["resposta"]
        gabarito_texto = q["alternativas"][gabarito]

        if resp_user == gabarito:
            st.markdown(f"""
            <div class='resultado-correto'>
                <strong>✅ Resposta correta!</strong> Alternativa {gabarito}: {gabarito_texto}
            </div>
            """, unsafe_allow_html=True)
        elif resp_user:
            resp_texto = q["alternativas"].get(resp_user, "")
            st.markdown(f"""
            <div class='resultado-errado'>
                <strong>❌ Resposta incorreta.</strong> Você marcou <strong>{resp_user}</strong>: {resp_texto}<br>
                <strong>Gabarito: {gabarito}</strong>: {gabarito_texto}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='resultado-correto' style='background:#EEF2FF; border-color:#4F46E5;'>
                <strong>📋 Gabarito:</strong> Alternativa {gabarito}: {gabarito_texto}
            </div>
            """, unsafe_allow_html=True)

        with st.expander("💡 Ver Explicação"):
            st.markdown(f"""
            <div class='explicacao-box'>
            {q['explicacao']}
            </div>
            """, unsafe_allow_html=True)

    # Mini mapa de questões
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    st.markdown("<p style='color:#000000; font-weight:700;'>Mapa de Questões (clique para navegar):</p>", unsafe_allow_html=True)

    cols_mapa = st.columns(10)
    for i, qmap in enumerate(questoes):
        col_idx = i % 10
        with cols_mapa[col_idx]:
            respondida = qmap["id"] in st.session_state.respondidas
            atual_flag = i == idx
            cor = "🟢" if respondida else ("🔵" if atual_flag else "⚪")
            if st.button(f"{cor}", key=f"nav_{i}", help=f"Q{qmap['id']} - {qmap['area']}"):
                st.session_state.questao_atual = i
                st.rerun()

    # Botão finalizar
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    col_f1, col_f2, col_f3 = st.columns([2, 2, 2])
    with col_f2:
        respondidas_count = len([q for q in PRIMEIRA_FASE if q["id"] in st.session_state.respondidas])
        if st.button(f"🏁 Finalizar 1ª Fase ({respondidas_count}/{len(PRIMEIRA_FASE)})", use_container_width=True):
            st.session_state.finalizado = True
            st.rerun()

# ─── RESULTADO FINAL 1ª FASE ──────────────────────────────────────────────────
elif st.session_state.fase == "1a" and st.session_state.finalizado:
    corretas, total, por_area = calcular_resultados()
    percentual = (corretas / total * 100) if total > 0 else 0
    nota = corretas * 2.5  # 40 questões * 2.5 = 100 pontos

    # Classificação
    if percentual >= 70:
        status = "🏆 APROVÁVEL!"
        status_cor = "#1B7F3B"
        status_bg = "#D4EDDA"
    elif percentual >= 50:
        status = "⚡ BOM DESEMPENHO"
        status_cor = "#C8962A"
        status_bg = "#FFF3CD"
    else:
        status = "📚 CONTINUE ESTUDANDO"
        status_cor = "#B71C1C"
        status_bg = "#FFEBEE"

    st.markdown(f"""
    <div class='score-final'>
        <div style='font-size:1rem; text-transform:uppercase; letter-spacing:2px; opacity:0.8; margin-bottom:0.5rem;'>Resultado Final</div>
        <div class='score-nota'>{corretas}/{total}</div>
        <div style='font-size:1.3rem; margin:0.5rem 0;'>{percentual:.1f}% de acerto</div>
        <div style='font-size:2rem; font-weight:700; margin:0.5rem 0;'>Nota: {nota:.1f}/100</div>
        <div style='display:inline-block; background:rgba(255,255,255,0.2); padding:8px 20px; border-radius:20px; font-size:1.1rem; font-weight:700;'>{status}</div>
        <div style='margin-top:1rem; opacity:0.8; font-size:0.9rem;'>Tempo total: {tempo_decorrido()}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

    # Desempenho por área
    st.markdown("### 📊 Desempenho por Área")
    areas_sorted = sorted(por_area.items(), key=lambda x: x[1]["corretas"]/x[1]["total"] if x[1]["total"] > 0 else 0, reverse=True)

    for area, dados in areas_sorted:
        pct_area = (dados["corretas"] / dados["total"] * 100) if dados["total"] > 0 else 0
        cor_barra = "#1B7F3B" if pct_area >= 70 else ("#C8962A" if pct_area >= 50 else "#B71C1C")
        col_a, col_b = st.columns([3, 1])
        with col_a:
            st.markdown(f"**{area}** — {dados['corretas']}/{dados['total']} questões")
            st.progress(pct_area / 100)
        with col_b:
            st.markdown(f"<div style='text-align:right; font-size:1.3rem; font-weight:700; color:{cor_barra}; padding-top:0.3rem;'>{pct_area:.0f}%</div>", unsafe_allow_html=True)

    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

    # Revisão das questões erradas
    erradas = [q for q in PRIMEIRA_FASE if st.session_state.respostas.get(q["id"]) != q["resposta"] and q["id"] in st.session_state.respondidas]
    if erradas:
        st.markdown(f"### ❌ Questões para Revisar ({len(erradas)})")
        for q in erradas:
            with st.expander(f"Q{q['id']} — {q['area']}"):
                st.markdown(f"<div style='color:#000000 !important;'>{q['enunciado']}</div>", unsafe_allow_html=True)
                resp_user = st.session_state.respostas.get(q["id"], "Não respondida")
                st.markdown(f"""
                <div class='resultado-errado'>
                    <strong>Sua resposta:</strong> {resp_user} — {q['alternativas'].get(resp_user, '')}<br>
                    <strong>Gabarito correto:</strong> {q['resposta']} — {q['alternativas'][q['resposta']]}
                </div>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                <div class='explicacao-box'>
                💡 <strong>Explicação:</strong> {q['explicacao']}
                </div>
                """, unsafe_allow_html=True)

    col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
    with col_r2:
        if st.button("🔄 Refazer 1ª Fase", use_container_width=True):
            resetar_simulado()
            st.session_state.fase = "1a"
            st.session_state.inicio = datetime.now()
            st.rerun()
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🏠 Voltar ao Início", use_container_width=True):
            resetar_simulado()
            st.rerun()

# ─── SEGUNDA FASE ─────────────────────────────────────────────────────────────
elif st.session_state.fase == "2a":
    st.markdown("""
    <div class='fuvest-header' style='border-left:none; background: linear-gradient(135deg, #7B4F00, #C8962A);'>
        <div class='fuvest-badge' style='background:#003082;'>2ª Fase • Dissertativa</div>
        <h1>Segunda Fase</h1>
        <p>Questões dissertativas e Redação — elabore suas respostas e compare com o gabarito</p>
    </div>
    """, unsafe_allow_html=True)

    idx = st.session_state.questao_atual
    q = SEGUNDA_FASE[idx]

    # Navegação
    col_prev, col_info, col_next = st.columns([1, 3, 1])
    with col_prev:
        if idx > 0:
            if st.button("◀ Anterior"):
                st.session_state.questao_atual = idx - 1
                st.rerun()
    with col_info:
        st.markdown(f"""
        <div style='text-align:center; padding:0.5rem; color:#6B7280;'>
            <strong>Questão {idx+1}</strong> de {len(SEGUNDA_FASE)} — {q['area']}
        </div>
        """, unsafe_allow_html=True)
    with col_next:
        if idx < len(SEGUNDA_FASE) - 1:
            if st.button("Próxima ▶"):
                st.session_state.questao_atual = idx + 1
                st.rerun()

    # Tabs de questões
    tabs_labels = [f"Q{i+1}" for i in range(len(SEGUNDA_FASE))]
    tab_cols = st.columns(len(SEGUNDA_FASE))
    for i, tc in enumerate(tab_cols):
        with tc:
            respondida = i in st.session_state.segunda_respostas
            icon = "✅" if respondida else "📝"
            if st.button(f"{icon} Q{i+1}", key=f"tab2f_{i}", use_container_width=True):
                st.session_state.questao_atual = i
                st.rerun()

    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)

    # Card da questão
    st.markdown(f"""
    <div class='questao-card' style='border-left-color: #C8962A;'>
        <div class='questao-numero'>✍️ {q['titulo']}</div>
        <div class='area-badge' style='background:#FFF3CD; color:#C8962A;'>📚 {q['area']}</div>
    """, unsafe_allow_html=True)

    st.markdown(f"<div style='color:#000000 !important;'>{q['enunciado']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Área de resposta
    st.markdown("#### 📝 Sua Resposta:")
    resp_key = f"resp_2f_{idx}"
    resp_atual = st.session_state.segunda_respostas.get(idx, "")

    if q.get("tipo") == "redacao":
        placeholder_text = "Escreva sua redação aqui...\n\nLembre-se da estrutura:\n• Introdução: apresente o tema e sua tese\n• Desenvolvimento: 2 ou mais parágrafos com argumentos\n• Conclusão: retome a tese e apresente proposta de intervenção detalhada"
        altura = 400
    else:
        placeholder_text = "Escreva sua resposta dissertativa aqui...\n\nDica: responda cada item (a, b, c...) separadamente."
        altura = 300

    resposta = st.text_area(
        "Sua resposta:",
        value=resp_atual,
        height=altura,
        placeholder=placeholder_text,
        key=resp_key,
        label_visibility="collapsed"
    )

    if resposta:
        st.session_state.segunda_respostas[idx] = resposta
        palavras = len(resposta.split())
        st.markdown(f"<div style='color:#6B7280; font-size:0.8rem; text-align:right;'>📊 {palavras} palavras | {len(resposta)} caracteres</div>", unsafe_allow_html=True)

    # Botão gabarito
    col_g1, col_g2, col_g3 = st.columns([2, 2, 2])
    with col_g2:
        if st.button("📋 Ver Gabarito / Resolução", use_container_width=True, key=f"gab_{idx}"):
            st.session_state.gabarito_2f_visivel.add(idx)

    if idx in st.session_state.gabarito_2f_visivel:
        st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
        st.markdown("#### ✅ Gabarito e Resolução Modelo:")
        st.markdown(f"""
        <div class='gabarito-box'>
        """, unsafe_allow_html=True)
        st.markdown(q["gabarito"])
        st.markdown("</div>", unsafe_allow_html=True)

        if resp_atual:
            st.markdown("#### 🔍 Autoavaliação:")
            st.markdown("""
            <div style='background:#EEF2FF; border-radius:12px; padding:1rem 1.5rem; border-left:4px solid #4F46E5;'>
            Compare sua resposta com o gabarito e avalie:
            </div>
            """, unsafe_allow_html=True)

            col_av1, col_av2, col_av3 = st.columns(3)
            with col_av1:
                st.markdown("**✅ Abordei os pontos principais?**")
            with col_av2:
                st.markdown("**📐 Minha estrutura foi adequada?**")
            with col_av3:
                st.markdown("**💡 Posso melhorar minha resposta?**")

    # Barra de progresso
    respondidas_2f = len(st.session_state.segunda_respostas)
    st.markdown("<div class='separator'></div>", unsafe_allow_html=True)
    st.markdown(f"**Progresso:** {respondidas_2f}/{len(SEGUNDA_FASE)} questões iniciadas")
    st.progress(respondidas_2f / len(SEGUNDA_FASE))

    col_fim1, col_fim2, col_fim3 = st.columns([2, 2, 2])
    with col_fim2:
        if st.button("🏠 Voltar ao Início", use_container_width=True):
            resetar_simulado()
            st.rerun()