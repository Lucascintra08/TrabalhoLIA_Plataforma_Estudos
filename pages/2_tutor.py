# pages/2_📚_Tutor.py
import streamlit as st
from src.models import StudyConfig
from src.services.pdf_utils import extrair_texto_arquivo
from src.agents.tutor_agent import gerar_resumo, gerar_questoes
from src.ui.sidebar import hide_default_multipage_nav, render_sidebar

hide_default_multipage_nav()
render_sidebar()

st.header("📚 Gerador de resumos e questões")

if "config" not in st.session_state:
    st.error("Configuração não carregada. Volte à página inicial.")
else:
    config: StudyConfig = st.session_state["config"]

    uploaded_file = st.file_uploader(
        "Envie um arquivo (PDF ou TXT) com o conteúdo a estudar", type=["pdf", "txt"]
    )

    materia_escolhida = st.selectbox(
        "Matéria para este conteúdo",
        options=config.materias or ["Matemática", "Português", "Física"],
    )

    modo = st.selectbox("O que você quer gerar?", ["Resumo", "Questões"])
    n_questoes = st.slider("Número de questões (se modo = Questões)", 1, 20, 5)

    if st.button("Gerar saída com IA"):
        if uploaded_file is None:
            st.warning("Envie um arquivo primeiro.")
        else:
            with st.spinner("Lendo arquivo e chamando o modelo..."):
                texto = extrair_texto_arquivo(uploaded_file)
                if not texto.strip():
                    st.error("Não foi possível extrair texto do arquivo.")
                else:
                    if modo == "Resumo":
                        saida = gerar_resumo(
                            texto,
                            nivel=config.nivel,
                            materia=materia_escolhida,
                        )
                    else:
                        saida = gerar_questoes(
                            texto,
                            n_questoes=n_questoes,
                            nivel=config.nivel,
                            materia=materia_escolhida,
                        )
            st.subheader("Resultado")
            st.markdown(saida)
