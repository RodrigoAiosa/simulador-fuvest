# 🎓 Simulador FUVEST 2025

Simulador completo e interativo das provas da FUVEST 2025, contemplando 1ª e 2ª fase, desenvolvido com Python e Streamlit.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação e Execução](#instalação-e-execução)
- [Configuração do Tema](#configuração-do-tema)
- [Conteúdo Programático](#conteúdo-programático)
- [Modos de Uso](#modos-de-uso)
- [Funcionalidades](#funcionalidades)
- [Correções e Melhorias Realizadas](#correções-e-melhorias-realizadas)
- [Estrutura de Arquivos](#estrutura-de-arquivos)

---

## 🔍 Visão Geral

O Simulador FUVEST 2025 é uma aplicação web local que replica a experiência das provas da FUVEST, permitindo ao candidato treinar tanto a 1ª fase (questões de múltipla escolha) quanto a 2ª fase (questões dissertativas e redação), com cronômetro, gabarito e explicações.

---

## 🗂️ Estrutura do Projeto

```
simulador-fuvest/
├── app.py                  # Arquivo principal da aplicação
├── questoes.py             # Banco de questões (1ª e 2ª fase)
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
└── .streamlit/
    └── config.toml         # Configuração do tema do Streamlit
```

---

## ✅ Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Navegador moderno (Chrome, Firefox, Edge)

---

## 🚀 Instalação e Execução

### 1. Clone ou baixe o projeto

```bash
git clone https://github.com/seu-usuario/simulador-fuvest-2025.git
cd simulador-fuvest-2025
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

Ou instale manualmente:

```bash
pip install streamlit>=1.32.0
```

### 3. Crie a pasta de configuração do tema

```bash
mkdir -p .streamlit
```

### 4. Execute a aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em:

```
http://localhost:8501
```

---

## ⚙️ Configuração do Tema

O arquivo `.streamlit/config.toml` é **obrigatório** para garantir a correta exibição dos textos com contraste adequado. Ele força o tema claro, evitando que o Streamlit aplique o tema escuro do sistema operacional sobre os textos das questões.

**Caminho:** `.streamlit/config.toml`

```toml
[theme]
base = "light"
textColor = "#000000"
backgroundColor = "#F0F2F8"
secondaryBackgroundColor = "#E8EBF5"
```

> ⚠️ **Atenção:** Sem esse arquivo, dependendo das configurações do sistema, os textos das questões podem aparecer com cor clara sobre fundo claro, tornando a leitura impossível.

---

## 📚 Conteúdo Programático

### 1ª Fase — 40 questões de múltipla escolha

| Disciplina | Tópicos Abordados |
|---|---|
| Português | Literatura brasileira e gramática |
| Matemática | Álgebra, geometria, probabilidade, logaritmos |
| Biologia | Genética, ecologia, bioquímica |
| Química | Tabela periódica, reações, estequiometria |
| Física | Mecânica, eletromagnetismo, óptica |
| História | Brasil e mundo |
| Geografia | Geografia física e humana |
| Filosofia e Sociologia | Pensamento crítico e sociedade |
| Inglês | Interpretação de texto em inglês |

### 2ª Fase — 8 questões dissertativas

| Nº | Área | Tema |
|---|---|---|
| 1 | Português e Redação | Interpretação textual |
| 2 | Matemática | Cálculo diferencial |
| 3 | Física | Eletricidade |
| 4 | Química | Química orgânica e estequiometria |
| 5 | Biologia | Genética mendeliana |
| 6 | História / Geografia | Brasil contemporâneo |
| 7 | Matemática | Trigonometria aplicada |
| 8 | Redação | Dissertativo-argumentativa |

---

## 🎯 Modos de Uso

### 🧪 Modo Simulado
- Sem exibição de gabarito durante a realização da prova
- Cronômetro ativo
- Experiência fiel ao dia da prova
- Resultado completo ao finalizar

### 📖 Modo Estudo
- Gabarito exibido imediatamente após cada resposta
- Explicações detalhadas para cada questão
- Ideal para revisão e aprendizado

---

## 🛠️ Funcionalidades

- **Navegação entre questões** com botões Anterior / Próxima e mapa de questões clicável
- **Cronômetro** em tempo real durante o simulado
- **Filtro por área** do conhecimento na barra lateral
- **Progresso visual** com contagem de questões respondidas
- **Gabarito completo** com percentual de acertos por disciplina ao final
- **Revisão das questões erradas** com explicação detalhada
- **Área de resposta dissertativa** com contador de palavras e caracteres (2ª fase)
- **Interface responsiva** compatível com desktop e mobile

---

## 🔧 Correções e Melhorias Realizadas

### Problema 1 — Texto das questões ilegível na 2ª Fase

**Descrição do problema:**
Após iniciar a 2ª fase, o enunciado das questões dissertativas aparecia com cor de texto clara (quase branca) sobre o fundo claro da página, tornando a leitura praticamente impossível.

**Causa raiz:**
O Streamlit, dependendo das configurações do sistema operacional do usuário, aplica automaticamente um tema escuro que sobrescreve as definições de cor do CSS da aplicação. A variável CSS `var(--texto)` utilizada na classe `.enunciado-texto` não estava sendo respeitada.

**Correções aplicadas:**

1. **`app.py` — Classe `.enunciado-texto`:**
   - Substituída a variável `color: var(--texto)` por `color: #000000 !important`
   - Adicionado `color: #000000 !important` em todos os elementos filhos via seletor `.enunciado-texto *`

2. **`app.py` — CSS Global:**
   - Adicionada cor preta forçada para os seletores `.main .block-container p`, `div`, `span`, `li`, `.stMarkdown` e `.element-container`, garantindo que nenhum texto da área principal seja afetado pelo tema do sistema

3. **`app.py` — Tag `html, body, .stApp`:**
   - Inserido `color: #000000 !important` diretamente na regra base do app

4. **`.streamlit/config.toml` — Arquivo de configuração de tema (novo arquivo):**
   - Criado arquivo de configuração explícita do Streamlit definindo `base = "light"` e `textColor = "#000000"`, impedindo que o Streamlit detecte e aplique o tema escuro do sistema operacional

**Linhas modificadas no `app.py`:**

```python
# Antes (problemático):
.enunciado-texto {
    color: var(--texto);   # variável ignorada pelo tema escuro
}

# Depois (corrigido):
.enunciado-texto {
    color: #000000 !important;
}
.enunciado-texto * {
    color: #000000 !important;
}
```

**Resultado:** Todos os textos de enunciado das questões passaram a ser exibidos em preto `#000000` independentemente do tema do sistema operacional.

---

### Problema 2 — Texto ilegível na revisão de questões erradas (1ª Fase)

**Descrição do problema:**
Na tela de resultados da 1ª fase, ao expandir a revisão de questões erradas, o enunciado da questão também aparecia com texto ilegível.

**Causa raiz:**
A linha de renderização do enunciado nessa seção utilizava `st.markdown(q["enunciado"])` sem nenhuma definição de cor, ficando totalmente sujeita ao tema do Streamlit.

**Correção aplicada:**

```python
# Antes:
st.markdown(q["enunciado"])

# Depois:
st.markdown(f"<div style='color:#000000 !important;'>{q['enunciado']}</div>", unsafe_allow_html=True)
```

---

## 📁 Estrutura de Arquivos Detalhada

```
simulador-fuvest/
│
├── app.py
│   ├── CSS global e variáveis de tema
│   ├── Configuração de estado da sessão (st.session_state)
│   ├── Sidebar com navegação, cronômetro e filtros
│   ├── Tela inicial (seleção de fase e modo)
│   ├── Renderização da 1ª Fase (múltipla escolha)
│   ├── Tela de resultados e revisão da 1ª Fase
│   └── Renderização da 2ª Fase (dissertativa e redação)
│
├── questoes.py
│   ├── PRIMEIRA_FASE: lista de 40 questões com alternativas, gabarito e explicação
│   └── SEGUNDA_FASE: lista de 8 questões dissertativas com gabarito modelo
│
├── requirements.txt
│   └── streamlit>=1.32.0
│
└── .streamlit/
    └── config.toml          ← OBRIGATÓRIO para exibição correta dos textos
```

---

## 📌 Observações Finais

- O simulador roda **100% localmente**, sem necessidade de internet após a instalação
- Os dados de resposta ficam armazenados apenas na sessão atual (não há banco de dados)
- Para reiniciar o simulado, basta atualizar a página no navegador
- Compatível com Windows, macOS e Linux