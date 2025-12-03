# pages/3_progresso_coach.py
import streamlit as st
from src.models import StudyConfig, Progresso, SolvedQuestion
from src.agents.coach_agent import registrar_sessao_estudo, sugerir_plano_diario
from src.config import PROGRESSO_FILE
from src.services.file_store import save_model
from src.ui.sidebar import hide_default_multipage_nav, render_sidebar
from src.logic.analytics import contar_tags
from datetime import datetime
import pandas as pd 

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
        # transforma em DataFrame para ficar mais fácil de filtrar e visualizar
        df_sessoes = pd.DataFrame([s.model_dump() for s in progresso.sessions])

        # garante que a coluna materia existe (só por segurança)
        if "materia" in df_sessoes.columns:
            materias_disponiveis = sorted(df_sessoes["materia"].dropna().unique().tolist())
        else:
            materias_disponiveis = []

        # Filtro por matéria
        materia_filtro = st.selectbox(
            "Filtrar por matéria",
            options=["Todas"] + materias_disponiveis if materias_disponiveis else ["Todas"],
        )

        if materia_filtro != "Todas":
            df_filtrado = df_sessoes[df_sessoes["materia"] == materia_filtro]
        else:
            df_filtrado = df_sessoes

        # ordena por timestamp (se existir)
        if "timestamp" in df_filtrado.columns:
            df_filtrado = df_filtrado.sort_values("timestamp", ascending=False)

        st.dataframe(df_filtrado, use_container_width=True)

        if st.button("🗑️ Limpar todas as sessões de estudo"):
            progresso.sessions = []            # zera a lista
            st.session_state["progresso"] = progresso
            save_model(PROGRESSO_FILE, progresso)
            st.success("Todas as sessões de estudo foram removidas.")
            st.rerun()           
    else:
        st.info("Ainda não há sessões registradas.")

    st.markdown("---")
    st.subheader("Resumo dos estudos")

    if progresso.sessions:
        total_sessoes = len(progresso.sessions)
        total_minutos = sum(s.duracao_min for s in progresso.sessions)
        st.write(f"📌 Total de sessões: **{total_sessoes}**")
        st.write(f"⏱️ Tempo total estudado: **{total_minutos} minutos** (~{total_minutos/60:.1f} horas)")
    else:
        st.write("Ainda não há dados suficientes para resumo.")


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

    if progresso.sessions:
        ultima = max(s.timestamp for s in progresso.sessions)
        dias = (datetime.now() - ultima).days
    else:
        dias = None

    if dias is None:
        st.info("Você ainda não registrou sessões. Bora começar!")
    elif dias == 0:
        st.success("Você estudou hoje! 👏 Continue assim.")
    elif dias <= 2:
        st.warning(f"Você está {dias} dia(s) sem estudar.")
    else:
        st.error(f"Você está há {dias} dias sem estudar. Vamos retomar?")

    tags = contar_tags(questoes_resolvidas)

    if st.button("Gerar sugestão com IA"):
        with st.spinner("Gerando..."):
            plano = sugerir_plano_diario(config, progresso, questoes_resolvidas, tags)
        st.markdown(plano)
    
    

