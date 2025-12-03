import streamlit as st
import json

from src.config import CONFIG_FILE, PROGRESSO_FILE, QUESTOES_FILE
from src.models import StudyConfig, Progresso, SolvedQuestion
from src.services.file_store import load_model
from src.ui.sidebar import hide_default_multipage_nav, render_sidebar

st.set_page_config(
    page_title="Plataforma de Estudos com IA",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

hide_default_multipage_nav()
render_sidebar()

# ---------- CARREGAR ESTADO GLOBAL ----------
if "config" not in st.session_state:
    config = load_model(
        CONFIG_FILE,
        model_cls=StudyConfig,
        default=StudyConfig(),
    )
    st.session_state["config"] = config

if "progresso" not in st.session_state:
    progresso = load_model(
        PROGRESSO_FILE,
        model_cls=Progresso,
        default=Progresso(),
    )
    st.session_state["progresso"] = progresso

if "questoes_resolvidas" not in st.session_state:
    if QUESTOES_FILE.exists():
        data = json.loads(QUESTOES_FILE.read_text(encoding="utf-8"))
        questoes = [SolvedQuestion.model_validate(q) for q in data]
    else:
        questoes = []
    st.session_state["questoes_resolvidas"] = questoes


# ---------- CONTEÚDO DA PÁGINA INICIAL ----------
st.title("🧠 Plataforma de Estudos com IA")

st.write("""
Bem-vindo!

Use o menu lateral para navegar entre:

- ⚙️ **Planejamento**
- 📚 **Gerador de resumos e questões**
- 📈 **Progresso dos Estudos**
- ❓ **Resolução de Questões**
""")
