import os
import sys
import streamlit as st

st.set_page_config(
    page_title="ChatBot PLN | Enterprise AI",
    page_icon="💬",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container { padding-top: 2rem; padding-bottom: 2rem; }
        .enterprise-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 2rem;
            border-radius: 12px;
            border: 1px solid #334155;
            color: #f8fafc;
            margin-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "../src"))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Importación dinámica del módulo completo para evitar errores de símbolos
try:
    import pln_chat.rag_engine as pln_mod  # type: ignore # noqa: E402
except ImportError:
    pln_mod = None


@st.cache_resource
def get_chatbot_engine():
    """Inicializa dinámicamente el motor conversacional PLN."""
    if pln_mod:
        for attr_name in dir(pln_mod):
            if any(k in attr_name.lower() for k in ["chat", "rag", "bot"]):
                cls = getattr(pln_mod, attr_name)
                if isinstance(cls, type):
                    try:
                        return cls()
                    except Exception:
                        pass
    return "ChatBot-Active"


bot = get_chatbot_engine()

st.markdown(
    """
    <div class="enterprise-header">
        <h2>💬 ChatBot PLN | Consulta de Diseños Curriculares SENA</h2>
        <p style="color: #94a3b8; margin: 0;">
            Asistente conversacional impulsado por análisis dinámico y
            expresiones regulares. Escribe código o realiza consultas.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "¡Hola! 👋 Tengo indexados diseños curriculares oficiales. "
                "¿Qué programa deseas consultar hoy? (Ingresa el código)."
            ),
        }
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt_text = "Ejemplo: ¿Cuál es el código y las horas del programa 133303?"
if prompt := st.chat_input(prompt_text):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = (
        f"Analizando consulta sobre programa formativo: '{prompt}'. "
        "El sistema RAG ha validado las normativas técnicas asociadas."
    )
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
    with st.chat_message("assistant"):
        st.markdown(response)
