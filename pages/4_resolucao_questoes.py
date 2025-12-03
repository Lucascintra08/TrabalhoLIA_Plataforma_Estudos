# pages/4_❓_Resolucao_de_Questoes.py
import streamlit as st
from src.models import StudyConfig, SolvedQuestion
from src.agents.question_solver_agent import resolver_questao
from src.ui.sidebar import hide_default_multipage_nav, render_sidebar
import pandas as pd 

hide_default_multipage_nav()
render_sidebar()

st.header("❓Resolução de Questões")

if "config" not in st.session_state or "questoes_resolvidas" not in st.session_state:
    st.error("Configuração ou histórico de questões não carregados. Volte à página inicial.")
else:
    config: StudyConfig = st.session_state["config"]
    questoes_resolvidas: list[SolvedQuestion] = st.session_state["questoes_resolvidas"]

    materia_q = st.text_input("Matéria / tema (ex: Matemática, História, Biologia)", "")
    enunciado_q = st.text_area("Enunciado da questão")
    alternativas_q = st.text_area(
        "Alternativas (opcional, uma por linha, ex: A) ..., B) ...)",
        "",
    )
    resposta_aluno_q = st.text_input("Sua resposta (ex: A, B, C ou texto livre)", "")

    if st.button("Corrigir e explicar"):
        if not enunciado_q.strip():
            st.warning("Preencha o enunciado da questão.")
        else:
            with st.spinner("Analisando a questão com IA..."):
                correcao, questoes_resolvidas = resolver_questao(
                    enunciado=enunciado_q,
                    alternativas=alternativas_q if alternativas_q.strip() else None,
                    resposta_aluno=resposta_aluno_q if resposta_aluno_q.strip() else None,
                    materia=materia_q if materia_q.strip() else None,
                    nivel=config.nivel,
                    questoes_existentes=questoes_resolvidas,
                )
            st.session_state["questoes_resolvidas"] = questoes_resolvidas
            st.subheader("Correção e comentários")
            st.markdown(correcao)

    st.markdown("---")
    st.subheader("Histórico completo de questões")

    if questoes_resolvidas:
        df_q = pd.DataFrame([q.model_dump() for q in questoes_resolvidas])

        # Garante que as colunas existam
        col_materia = "materia" if "materia" in df_q.columns else None
        col_timestamp = "timestamp" if "timestamp" in df_q.columns else None

        # Filtro por matéria (se houver coluna materia)
        if col_materia:
            materias_q = sorted(df_q[col_materia].dropna().unique().tolist())
            materia_filtro_q = st.selectbox(
                "Filtrar questões por matéria",
                options=["Todas"] + materias_q if materias_q else ["Todas"],
            )

            if materia_filtro_q != "Todas":
                df_q_filtrado = df_q[df_q[col_materia] == materia_filtro_q]
            else:
                df_q_filtrado = df_q
        else:
            df_q_filtrado = df_q

        # Ordena por timestamp se existir
        if col_timestamp:
            df_q_filtrado = df_q_filtrado.sort_values(col_timestamp, ascending=False)

        # Mostra só colunas principais para não ficar poluído
        colunas_para_mostrar = [
            c for c in df_q_filtrado.columns
            if c in ["timestamp", "materia", "enunciado", "resposta_aluno"]
        ]
        if colunas_para_mostrar:
            st.dataframe(df_q_filtrado[colunas_para_mostrar], use_container_width=True)
        else:
            st.dataframe(df_q_filtrado, use_container_width=True)
    else:
        st.info("Ainda não há questões registradas no histórico.")
