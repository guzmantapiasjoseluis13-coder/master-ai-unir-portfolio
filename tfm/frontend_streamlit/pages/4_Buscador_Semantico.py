import os
import sys
import streamlit as st

st.set_page_config(
    page_title="Buscador Semántico | Enterprise AI",
    page_icon="🔍",
    layout="wide",
)

st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .enterprise-header {
            background: linear-gradient(
                135deg, #0f172a 0%, #1e293b 100%
            );
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
pln_chat_dir = os.path.abspath(os.path.join(current_dir, "../src/pln_chat"))

for target_path in [src_dir, pln_chat_dir]:
    if target_path not in sys.path:
        sys.path.insert(0, target_path)

try:
    import semantic_search as sem_mod  # type: ignore # noqa: E402
except Exception as err:
    sem_mod = None
    st.error(f"❌ Error al importar backend: {err}")


@st.cache_data
def cargar_corpus_desde_archivo():
    """Lee dinámicamente el archivo local y separa texto y URL."""
    possible_paths = [
        os.path.join(current_dir, "../data/raw/oferta_medellin.txt"),
        os.path.join(current_dir, "../data/oferta_medellin.txt"),
        os.path.join(current_dir, "../../data/raw/oferta_medellin.txt"),
        "oferta_medellin.txt",
    ]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                lines = f.readlines()
                parsed_data = []
                for line in lines:
                    if line.strip():
                        parts = line.strip().split("|")
                        texto = parts[0].strip()
                        if len(parts) > 1:
                            url = parts[1].strip()
                        else:
                            q_enc = texto.replace(" ", "+")
                            base_url = "https://www.google.com" "/search?q="
                            url = base_url + q_enc
                        parsed_data.append(
                            {
                                "texto": texto,
                                "url": url,
                            }
                        )
                return parsed_data
    return []


corpus_local = cargar_corpus_desde_archivo()

with st.sidebar:
    st.markdown("### ⚙️ Configuración IR")
    p_blog1 = "Extrae artículos en "
    p_blog2 = "tiempo real de "
    p_blog3 = "sena-comercio.blogspot.com"
    blog_help_msg = p_blog1 + p_blog2 + p_blog3

    incluir_blog = st.checkbox(
        "Incluir Blog Centro de Comercio",
        value=True,
        help=blog_help_msg,
    )
    top_k = st.slider(
        "Resultados Top-K",
        min_value=1,
        max_value=5,
        value=3,
    )
    st.markdown("---")
    info_sidebar = (
        "**Motor Vectorial Activo**\n\n"
        + "Combinando corpus institucional "
        + "y entradas del blog SENA."
    )
    st.info(info_sidebar)


@st.cache_resource
def obtener_buscador(model_name="all-MiniLM-L6-v2"):
    """Instancia el motor vectorial."""
    if sem_mod and hasattr(sem_mod, "BuscadorVectorial"):
        return sem_mod.BuscadorVectorial(model_name=model_name)
    return None


buscador = obtener_buscador()

if buscador and hasattr(buscador, "indexar_corpus"):
    buscador.indexar_corpus(
        corpus_local=corpus_local,
        incluir_blog=incluir_blog,
    )

st.markdown(
    """
    <div class="enterprise-header">
        <h2>🔍 Módulo Enterprise: Buscador Vectorial</h2>
        <p style="color: #94a3b8; margin: 0;">
            Cátedra PLN: Recuperación de información
            con espacios vectoriales y Coseno.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs(
    [
        "💬 Consulta Semántica",
        "📊 Espacio Vectorial 2D",
        "⚙️ Arquitectura & Métricas",
    ]
)

with tab1:
    with st.container(border=True):
        st.markdown("### 🔎 Ingrese su consulta semántica:")
        q1 = "Ej: tecnología, inscripciones, "
        q2 = "contrato de aprendizaje, CDMC..."
        ph_text = q1 + q2

        query = st.text_input(
            "Consulta",
            placeholder=ph_text,
            label_visibility="collapsed",
        )

        if not query:
            st.info(
                "👋 **Bienvenido al motor (IR).**\n"
                + "Ingrese un término clave o concepto "
                + "para consultar similitudes."
            )
        else:
            if not buscador or not hasattr(buscador, "buscar"):
                e1 = "⚠️ El motor backend "
                e2 = "no está disponible\n"
                e3 = "o incompleto."
                err_msg = e1 + e2 + e3
                st.warning(err_msg)
            else:
                res_tuple = buscador.buscar(query, top_k=top_k)
                resultados, q_2d, score_prom = res_tuple

                if resultados:
                    m1 = "✅ **Búsqueda Exitosa** "
                    m2 = f"(Promedio: {score_prom:.4f})"
                    msg_ex = m1 + m2
                    st.success(msg_ex)

                    for i, res in enumerate(resultados, 1):
                        score_val = res["score"]
                        texto_res = res["texto"]
                        url_res = res["url"]

                        with st.container(border=True):
                            ps1 = f"**{i}. "
                            ps2 = "[Coseno: "
                            ps3 = f"{score_val:.4f}]**"
                            prefix_score = ps1 + ps2 + ps3
                            st.markdown(prefix_score)
                            st.write(texto_res)

                            l1 = "🔗 **[Sitio Oficial / "
                            l2 = f"Fuente]**({url_res})"
                            link_txt = l1 + l2
                            st.markdown(link_txt)
                else:
                    mw1 = "⚠️ No se hallaron "
                    mw2 = f"resultados para '{query}'."
                    msg_w = mw1 + mw2
                    st.warning(msg_w)

with tab2:
    with st.container(border=True):
        st.markdown("### 📈 Proyección Bidimensional (PCA 2D)")
        st.write(
            "Visualización de los embeddings proyectados "
            + "a 2D para el corpus y la consulta."
        )

        if (
            buscador
            and hasattr(buscador, "corpus_2d")
            and buscador.corpus_2d is not None
            and len(buscador.corpus_2d) > 0
        ):
            import pandas as pd

            corpus_points = buscador.corpus_2d
            df_plot = pd.DataFrame(
                corpus_points,
                columns=["PCA_1", "PCA_2"],
            )
            tipo_list = ["Documento / Blog" for _ in range(len(corpus_points))]
            df_plot["Tipo"] = tipo_list

            st.scatter_chart(
                df_plot,
                x="PCA_1",
                y="PCA_2",
                color="Tipo",
                use_container_width=True,
            )
            n_vec = len(corpus_points)
            info_txt = f"Total vectores en el espacio: {n_vec}"
            st.info(info_txt)
        else:
            plan_msg = "Indexe el corpus para " "visualizar el plano 2D."
            st.info(plan_msg)

with tab3:
    with st.container(border=True):
        st.markdown("### 📐 Especificaciones Matemáticas")
        st.write(
            "- **Modelo Base:** Sentence-Transformers "
            + "(`all-MiniLM-L6-v2`).\n"
            + "- **Métrica:** Similitud del Coseno.\n"
            + "- **Ingesta Híbrida:** Corpus local + "
            + "Web Scraping del blog SENA "
            + "(`https://sena-comercio.blogspot.com/`).\n"
            + "- **Reducción:** PCA (2D)."
        )
