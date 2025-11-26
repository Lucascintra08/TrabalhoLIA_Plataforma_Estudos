# pages/4_❓_Resolucao_de_Questoes.py
import streamlit as st
from src.models import StudyConfig, SolvedQuestion
from src.agents.question_solver_agent import resolver_questao
from src.ui.sidebar import hide_default_multipage_nav, render_sidebar

hide_default_multipage_nav()
render_sidebar()

st.header("❓ Agente de Resolução de Questões")

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
    st.subheader("Histórico recente de questões resolvidas")
    if questoes_resolvidas:
        ultimas = list(reversed(questoes_resolvidas))[:5]
        for q in ultimas:
            st.markdown(f"**{q.timestamp}** – {q.enunciado[:150]}...")
    else:
        st.info("Ainda não há questões resolvidas registradas.")
