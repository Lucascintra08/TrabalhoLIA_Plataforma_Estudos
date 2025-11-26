# pages/1_⚙️_Planejamento.py
import streamlit as st
from src.models import StudyConfig
from src.config import CONFIG_FILE
from src.services.file_store import save_model
from src.ui.sidebar import hide_default_multipage_nav, render_sidebar

hide_default_multipage_nav()
render_sidebar()

st.header("⚙️ Planejamento de Estudos")

# Garante que config existe no session_state
if "config" not in st.session_state:
    st.error("Configuração não carregada. Volte à página inicial.")
else:
    config: StudyConfig = st.session_state["config"]

    nivel = st.selectbox(
        "Nível de ensino",
        ["Ensino Fundamental", "Ensino Médio", "Ensino Superior"],
        index=["Ensino Fundamental", "Ensino Médio", "Ensino Superior"].index(
            config.nivel if config.nivel in ["Ensino Fundamental", "Ensino Médio", "Ensino Superior"] else "Ensino Médio"
        ),
    )

    prova_alvo = st.text_input("Prova alvo", config.prova_alvo)
    horas_semana = st.number_input(
        "Horas de estudo por semana", 1, 100, config.horas_semana
    )
    materias_str = st.text_area(
        "Principais matérias (separadas por vírgula)",
        ", ".join(config.materias),
    )

    if st.button("Salvar planejamento"):
        config.nivel = nivel
        config.prova_alvo = prova_alvo
        config.horas_semana = int(horas_semana)
        config.materias = [m.strip() for m in materias_str.split(",") if m.strip()]

        st.session_state["config"] = config
        save_model(CONFIG_FILE, config)
        st.success("Planejamento salvo com sucesso!")

    st.subheader("Configuração atual")
    st.json(config.model_dump())
