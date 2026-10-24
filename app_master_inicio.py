# flake8: noqa: E203
import streamlit as st

st.set_page_config(
    page_title="TFM Enterprise Portfolio | Máster en IA - UNIR",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos CSS de Alta Gama (Dark Glassmorphism & Executive UI)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #05070B;
        color: #F3F4F6;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                     Roboto, Helvetica, Arial, sans-serif;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    .hero-executive {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.12) 0%,
                                           rgba(59, 130, 246, 0.12) 50%,
                                           rgba(139, 92, 246, 0.12) 100%);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 16px;
        padding: 40px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(8px);
    }

    .enterprise-card {
        background: rgba(17, 24, 39, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 22px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
        margin-bottom: 18px;
        transition: transform 0.2s ease;
    }

    .enterprise-card:hover {
        border-color: rgba(16, 185, 129, 0.4);
    }

    .metric-badge {
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #34D399;
        padding: 6px 12px;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 10px;
    }

    .section-header {
        border-left: 4px solid #10B981;
        padding-left: 12px;
        margin-top: 25px;
        margin-bottom: 18px;
        font-weight: 700;
        font-size: 1.3rem;
        color: #FFFFFF;
        letter-spacing: -0.01em;
    }

    .subject-pill {
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        font-size: 0.9rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Sidebar Ejecutivo
with st.sidebar:
    st.markdown(
        "### 🎓 **MÁSTER OFICIAL EN IA**\n"
        "*Universidad Internacional de La Rioja (UNIR)*"
    )
    st.markdown("---")
    st.markdown("#### 🚀 Módulos del Portafolio TFM")
    st.info(
        "Navegue a través de las páginas de la barra lateral para ejecutar "
        "los mini-proyectos de Visión Artificial y PLN."
    )
    st.markdown("---")
    st.markdown(
        "<div style='font-size: 0.82rem; color: #9CA3AF; line-height: 1.6;'>"
        "<b>Investigador / Autor:</b> Jose Luis Guzman Tapias<br>"
        "<b>Programa:</b> Máster Universitario en IA (60 ECTS)<br>"
        "<b>Escuela:</b> ESIT (Ingeniería y Tecnología)<br>"
        "<b>Entorno Académico:</b> UNIR (España / Colombia)<br>"
        "<b>Estado del Sistema:</b> <span style='color: #34D399;'>"
        "● Operativo [Producción]</span>"
        "</div>",
        unsafe_allow_html=True,
    )

# Header Principal (Hero Section)
st.markdown(
    """
    <div class='hero-executive'>
        <span class='metric-badge'>
            DEFENSA ACADÉMICA TFM • MASTER PORTFOLIO 2026
        </span>
        <h1 style='color: #FFFFFF; font-size: 2.6rem; margin-top: 10px;
                   margin-bottom: 12px;'>
            Plataforma Enterprise de Visión Artificial e Inteligencia
            Artificial
        </h1>
        <p style='color: #34D399; font-size: 1.2rem; font-weight: 600;'>
            Visión Computacional Avanzada, Modelos Vectoriales y PLN
            Institucional
        </p>
        <p style='color: #9CA3AF; font-size: 0.95rem; max-width: 800px;
                  margin: 0 auto;'>
            Desarrollo integral presentado para la culminación del Máster
            Universitario en Inteligencia Artificial de la UNIR, articulando
            rigor matemático, ingeniería de software y aplicación práctica.
        </p>
    </div>
""",
    unsafe_allow_html=True,
)

# Métricas Globales del Portafolio
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(
        "<div class='enterprise-card' style='text-align: center;'>"
        "<div style='font-size: 0.75rem; color: #9CA3AF;'>"
        "CRÉDITOS OFICIALES</div>"
        "<div style='font-size: 1.5rem; font-weight: 700; color: #34D399;'>"
        "60 ECTS</div></div>",
        unsafe_allow_html=True,
    )
with m2:
    st.markdown(
        "<div class='enterprise-card' style='text-align: center;'>"
        "<div style='font-size: 0.75rem; color: #9CA3AF;'>"
        "CÁTEDRAS DE BASE</div>"
        "<div style='font-size: 1.5rem; font-weight: 700; color: #60A5FA;'>"
        "VA & PLN</div></div>",
        unsafe_allow_html=True,
    )
with m3:
    st.markdown(
        "<div class='enterprise-card' style='text-align: center;'>"
        "<div style='font-size: 0.75rem; color: #9CA3AF;'>"
        "MODELOS DE INFERENCIA</div>"
        "<div style='font-size: 1.5rem; font-weight: 700; color: #A78BFA;'>"
        "YOLOv8 / Embeddings</div></div>",
        unsafe_allow_html=True,
    )
with m4:
    st.markdown(
        "<div class='enterprise-card' style='text-align: center;'>"
        "<div style='font-size: 0.75rem; color: #9CA3AF;'>"
        "CUMPLIMIENTO TÉCNICO</div>"
        "<div style='font-size: 1.5rem; font-weight: 700; color: #34D399;'>"
        "100% Zero-Hardcode</div></div>",
        unsafe_allow_html=True,
    )

# Pestañas de Presentación Ejecutiva
tab_defensa, tab_unir, tab_plan, tab_proyectos = st.tabs(
    [
        "🏛️ Marco del TFM y Visión",
        "🇪🇸 Origen y Red Global UNIR",
        "📚 Plan de Estudios Oficial",
        "🚀 Módulos Prácticos Desplegados",
    ]
)

with tab_defensa:
    st.markdown(
        "<div class='section-header'>"
        "Fundamentación Científica y Alcance del TFM</div>",
        unsafe_allow_html=True,
    )
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown(
            """
            <div class='enterprise-card'>
                <h4>🎯 Visión del Proyecto y Aporte Tecnológico</h4>
                <p style='font-size: 0.9rem; color: #D1D5DB;
                          line-height: 1.7;'>
                Este portafolio consolida los aprendizajes de la maestría
                en una solución de grado empresarial. Combina técnicas de
                <b>Procesamiento de Imágenes</b> (detección con YOLOv8, OCR en
                uniformes y trazabilidad espacial) con modelos de
                Procesamiento de Lenguaje Natural (<b>PLN</b>) basados en
                embeddings vectoriales y similitud cosenoidal.
                </p>
                <p style='font-size: 0.9rem; color: #D1D5DB;
                          line-height: 1.7;'>
                Diseñado bajo estrictos principios de modularidad y
                escalabilidad, el sistema elimina cualquier dependencia
                de código quemado (*hardcoding*), garantizando
                autonomía analítica.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with col_d2:
        st.markdown(
            """
            <div class='enterprise-card'>
                <h4>📊 Alineación con la Industria 4.0 y el SENA</h4>
                <p style='font-size: 0.9rem; color: #D1D5DB;
                          line-height: 1.7;'>
                La aplicación práctica implementada en el entorno
                institucional del <b>SENA Antioquia (Medellín)</b> demuestra
                la viabilidad de desplegar sistemas inteligentes de
                auditoría y trazabilidad educativa automatizada.
                </p>
                <ul style='font-size: 0.88rem; color: #9CA3AF;
                           line-height: 1.6; margin-top: 8px;'>
                    <li>Validación óptica de identidad y uniformes.</li>
                    <li>Búsqueda semántica sobre normativas institucionales.</li>
                    <li>Sistematización masiva de expedientes.</li>
                </ul>
            </div>
        """,
            unsafe_allow_html=True,
        )

with tab_unir:
    st.markdown(
        "<div class='section-header'>" "Excelencia Académica y Expansión Global</div>",
        unsafe_allow_html=True,
    )
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            <div class='enterprise-card'>
                <h4>🇪🇸 Sede Central y Rectorado (Logroño, España)</h4>
                <p style='font-size: 0.9rem; color: #D1D5DB;
                          line-height: 1.6;'>
                Fundada en La Rioja, la Universidad Internacional de La Rioja
                (UNIR) lidera el modelo de educación superior 100% online en
                el Espacio Europeo de Educación Superior (EEES). Con más de
                41,000 estudiantes y presencia consolidada en 90 países, la
                institución integra tecnología de punta para conectar talento
                global con rigor académico.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class='enterprise-card'>
                <h4>🇨🇴 Sede Regional y Proyección (Bogotá, Colombia)</h4>
                <p style='font-size: 0.9rem; color: #D1D5DB;
                          line-height: 1.6;'>
                Respaldada por el Ministerio de Educación Nacional (MEN), la
                delegación en Colombia articula la academia con las demandas
                del sector productivo latinoamericano, fomentando la
                investigación aplicada y la transformación digital.
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

with tab_plan:
    st.markdown(
        "<div class='section-header'>"
        "Itinerario Académico del Máster (60 ECTS)</div>",
        unsafe_allow_html=True,
    )
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown(
            """
            <div class='enterprise-card'>
                <h4 style='color: #34D399; margin-bottom: 15px;'>
                    📖 Primer Cuatrimestre
                </h4>
                <div class='subject-pill'>
                    <span>Investigación y Gestión de Proyectos en IA</span>
                    <span style='color: #34D399; font-weight: 700;'>
                        6 ECTS
                    </span>
                </div>
                <div class='subject-pill' style='border: 1px solid #10B981;
                     background: rgba(16, 185, 129, 0.12);'>
                    <span><b>Procesamiento del Lenguaje Natural (PLN)</b></span>
                    <span style='color: #34D399; font-weight: 700;'>
                        6 ECTS
                    </span>
                </div>
                <div class='subject-pill' style='border: 1px solid #10B981;
                     background: rgba(16, 185, 129, 0.12);'>
                    <span><b>Visión Artificial (Asignatura Base)</b></span>
                    <span style='color: #34D399; font-weight: 700;'>
                        6 ECTS
                    </span>
                </div>
                <div class='subject-pill'>
                    <span>Técnicas de Aprendizaje Automático</span>
                    <span style='color: #34D399; font-weight: 700;'>
                        6 ECTS
                    </span>
                </div>
                <div class='subject-pill'>
                    <span>Razonamiento y Planificación Automática</span>
                    <span style='color: #34D399; font-weight: 700;'>
                        6 ECTS
                    </span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with col_c2:
        st.markdown(
            """
            <div class='enterprise-card'>
                <h4 style='color: #60A5FA; margin-bottom: 15px;'>
                    📖 Segundo Cuatrimestre
                </h4>
                <div class='subject-pill'>
                    <span>Redes Neuronales y Aprendizaje Profundo</span>
                    <span style='color: #60A5FA; font-weight: 700;'>
                        6 ECTS
                    </span>
                </div>
                <div class='subject-pill'>
                    <span>Aprendizaje Automático no Supervisado</span>
                    <span style='color: #60A5FA; font-weight: 700;'>
                        6 ECTS
                    </span>
                </div>
                <div class='subject-pill'>
                    <span>Optativa / Prácticas Profesionales</span>
                    <span style='color: #60A5FA; font-weight: 700;'>
                        6 ECTS
                    </span>
                </div>
                <div class='subject-pill' style='border: 1px solid #60A5FA;
                     background: rgba(59, 130, 246, 0.12);'>
                    <span><b>Trabajo de Fin de Máster (TFM)</b></span>
                    <span style='color: #60A5FA; font-weight: 700;'>
                        12 ECTS
                    </span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

with tab_proyectos:
    st.markdown(
        "<div class='section-header'>"
        "Arquitectura de Módulos Desplegados en la Plataforma</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class='enterprise-card'>
            <h4>🚀 Subsistemas Integrados (Acceso en Barra Lateral):</h4>
            <ul style='color: #D1D5DB; font-size: 0.92rem; line-height: 1.8;'>
                <li><b>1. Vision Fénix AI (Cátedra Visión Artificial):</b>
                Pipeline de auditoría de uniformes, extracción de ROI por
                tensores, OCR neuronal y trazabilidad de expedientes.</li>
                <li><b>2. Buscador Semántico (Cátedra PLN):</b>
                Recuperación de información sobre corpus normativos basada en
                modelos vectoriales y similitud del coseno.</li>
            </ul>
        </div>
    """,
        unsafe_allow_html=True,
    )
