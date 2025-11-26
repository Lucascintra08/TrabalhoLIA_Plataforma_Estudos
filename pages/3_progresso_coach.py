# pages/3_progresso_coach.py
import streamlit as st
from src.models import StudyConfig, Progresso, SolvedQuestion
from src.agents.coach_agent import registrar_sessao_estudo, sugerir_plano_diario
from src.config import PROGRESSO_FILE
from src.services.file_store import save_model
from src.ui.sidebar import hide_default_multipage_nav, render_sidebar

hide_default_multipage_nav()
render_sidebar()

st.header("📈 Progresso dos Estudos")

if "config" not in st.session_state or "progresso" not in st.session_state:
    st.error("Configuração ou progresso não carregados. Volte à página inicial.")
else:
    config: StudyConfig = st.session_state["config"]
    progresso: Progresso = st.session_state["progresso"]
    questoes_resolvidas: list[SolvedQuestion] = st.session_state.get(
        "questoes_resolvidas", []
    )

    st.subheader("Sessões de estudo registradas")

    if progresso.sessions:
        st.table([s.model_dump() for s in progresso.sessions])

        if st.button("🗑️ Limpar todas as sessões de estudo"):
            progresso.sessions = []            # zera a lista
            st.session_state["progresso"] = progresso
            save_model(PROGRESSO_FILE, progresso)
            st.success("Todas as sessões de estudo foram removidas.")
            st.rerun()           
    else:
        st.info("Ainda não há sessões registradas.")

    st.markdown("---")
    st.subheader("Registrar nova sessão de estudo")

    materia_sessao = st.text_input("Matéria / tema estudado", "")
    duracao_sessao = st.number_input(
        "Duração (minutos)", min_value=10, max_value=600, value=50
    )
    obs_sessao = st.text_area("Observações (opcional)", "")

    if st.button("Registrar sessão"):
        if not materia_sessao.strip():
            st.warning("Informe a matéria/tema.")
        else:
            progresso = registrar_sessao_estudo(
                progresso, materia_sessao.strip(), int(duracao_sessao), obs_sessao
            )
            st.session_state["progresso"] = progresso
            save_model(PROGRESSO_FILE, progresso)
            st.success("Sessão registrada!")

    st.markdown("---")
    st.subheader("Sugestão de plano de estudo para hoje")

    if st.button("Gerar sugestão com IA"):
        with st.spinner("Gerando plano com IA..."):
            plano = sugerir_plano_diario(config, progresso, questoes_resolvidas)
        st.markdown(plano)
