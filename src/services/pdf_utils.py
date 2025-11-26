# src/services/pdf_utils.py
from pypdf import PdfReader


def extrair_texto_arquivo(uploaded_file) -> str:
    """
    Extrai texto de arquivo TXT ou PDF enviado pelo Streamlit.
    `uploaded_file` é o objeto retornado por st.file_uploader.
    """
    if uploaded_file is None:
        return ""

    nome = uploaded_file.name.lower()
    if nome.endswith(".txt"):
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if nome.endswith(".pdf"):
        reader = PdfReader(uploaded_file)
        texto = []
        for page in reader.pages:
            texto.append(page.extract_text() or "")
        return "\n".join(texto)

    # fallback: tentar decodificar como texto
    return uploaded_file.read().decode("utf-8", errors="ignore")
