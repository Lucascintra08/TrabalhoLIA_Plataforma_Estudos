# pages/2_📚_Tutor.py
import streamlit as st
import re

from src.models import StudyConfig
from src.services.pdf_utils import extrair_texto_arquivo
from src.agents.tutor_agent import gerar_resumo, gerar_questoes
from src.ui.sidebar import hide_default_multipage_nav, render_sidebar

# Ocultar menu nativo do Streamlit
hide_default_multipage_nav()
render_sidebar()

st.header("📚 Gerador de resumos e questões")


# -------------------------
# Função auxiliar: empilhar alternativas
# -------------------------
def empilhar_alternativas(texto: str) -> str:
    """
    Garante que alternativas do tipo 'A) ... B) ... C) ...'
    fiquem empilhadas em linhas separadas.
    Coloca quebra de linha antes de A), B), C), D), E) quando vierem em sequência.
    """
    # quebra linha antes de A), B), C), D), E) quando vierem após espaço
    texto = re.sub(r"\s([A-E])\)", r"\n\1)", texto)
    # opcional: garante uma linha em branco antes do GABARITO
    texto = re.sub(r"\nGABARITO", r"\n\nGABARITO", texto, flags=re.IGNORECASE)
    return texto


# -------------------------
# VERIFICAR CONFIGURAÇÃO
# -------------------------
if "config" not in st.session_state:
    st.error("Configuração não carregada. Volte à página inicial.")
    st.stop()

config: StudyConfig = st.session_state["config"]


# -------------------------
# INPUTS DA PÁGINA
# -------------------------
uploaded_file = st.file_uploader(
    "Envie um arquivo (PDF ou TXT) com o conteúdo a estudar",
    type=["pdf", "txt"],
)

materia_escolhida = st.selectbox(
    "Matéria para este conteúdo",
    options=config.materias or ["Matemática", "Português", "Física"],
)

modo = st.selectbox(
    "O que você quer gerar?",
    ["Resumo", "Questões"]
)

n_questoes = st.slider(
    "Número de questões (se modo = Questões)",
    1, 20, 5
)


# -------------------------
# BOTÃO PRINCIPAL
# -------------------------
if st.button("Gerar saída"):

    if uploaded_file is None:
        st.warning("Envie um arquivo primeiro.")
        st.stop()

    # Extração de texto
    with st.spinner("📄 Lendo arquivo enviado..."):
        texto = extrair_texto_arquivo(uploaded_file)

    if not texto.strip():
        st.error("Não foi possível extrair texto do arquivo.")
        st.stop()

    # ============================================================
    # 1) GERAR RESUMO
    # ============================================================
    if modo == "Resumo":
        with st.spinner("📝 Gerando resumo com IA..."):
            saida = gerar_resumo(
                texto,
                nivel=config.nivel,
                materia=materia_escolhida,
            )

        st.subheader("📝 Resumo Gerado")
        st.markdown(saida)

        st.download_button(
            "📥 Baixar resumo (.txt)",
            data=saida,
            file_name="resumo.txt",
            mime="text/plain",
        )
        st.stop()

    # ============================================================
    # 2) GERAR QUESTÕES (texto normal) + empilhar alternativas
    # ============================================================
    with st.spinner("🧠 Gerando questões com IA..."):
        saida_bruta = gerar_questoes(
            texto,
            n_questoes=n_questoes,
            nivel=config.nivel,
            materia=materia_escolhida,
        )

    # pós-processamento para empilhar alternativas
    saida_formatada = empilhar_alternativas(saida_bruta)

    st.subheader("🧠 Questões Geradas")
    st.markdown(saida_formatada)

    st.download_button(
        "📥 Baixar questões (.txt)",
        data=saida_formatada,
        file_name="questoes_geradas.txt",
        mime="text/plain",
    )
