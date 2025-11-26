# src/ui/sidebar.py
import streamlit as st

def hide_default_multipage_nav():
    """Esconde o menu multipage padrão do Streamlit."""
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                display: none;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_sidebar():
    """Desenha a sidebar personalizada da aplicação."""
    with st.sidebar:
        st.title("🧭 Navegação")

        # app.py (Home)
        st.page_link("app.py", label="🏠 Início")

        # Páginas internas (ajuste os nomes conforme seus arquivos)
        st.page_link("pages/1_planejamento.py", label="⚙️ Planejamento")
        st.page_link("pages/2_tutor.py", label="📚 Gerador de resumos e questões")
        st.page_link("pages/3_progresso_coach.py", label="📈 Progresso dos Estudos")
        st.page_link("pages/4_resolucao_questoes.py", label="❓ Resolução de Questões")
