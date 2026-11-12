# 🧩 Mini-Proyectos: Componentes Modulares de IA

Este directorio contiene los módulos funcionales de software que sirven como **entregables técnicos para las asignaturas del primer cuatrimestre** del Máster Universitario en Inteligencia Artificial (UNIR), y que a su vez actúan como **herramientas (SKILLs) y módulos de soporte para la arquitectura del Proyecto FÉNIX (TFM)**.

Cada mini-proyecto ha sido desarrollado bajo estándares de nivel *Enterprise* (PEP8, tipado estático, contenerización OCI, pruebas unitarias), demostrando competencias de ingeniería *Production-Ready*.

## 🗺️ Mapa de Articulación Académica y TFM

A continuación se detalla cómo cada componente se mapea a una asignatura específica y cómo alimenta la arquitectura FÉNIX (ORCH + CIE-01 + CIE-02).

| Mini-Proyecto | Asignatura UNIR (1er Cuatrimestre) | Aporte al TFM FÉNIX (Arquitectura) |
| :--- | :--- | :--- |
| **01_analitica_pdf** | *Técnicas de Aprendizaje Automático / Procesamiento de Datos* | **Motor de Conocimiento para CIE-01 y CIE-02.** Permite extraer metadatos de normativas y guías del SENA, alimentando el sistema RAG para evitar alucinaciones. |
| **02_pln_chat** | *Procesamiento del Lenguaje Natural (PLN)* | **Motor de Recuperación Semántica (RAG).** Proporciona a CIE-02 la capacidad de buscar respuestas en el corpus institucional usando embeddings vectoriales. |
| **03_vision_aprendices** | *Visión Artificial* | **SKILL de Validación Visual.** Otorga a los agentes la capacidad de procesar imágenes (ej. evidencias gráficas, formatos, credenciales) aplicando anonimización (RGPD). |
| **04_agentic_ai** | *Razonamiento y Planificación Automática* | **Núcleo del Orquestador (ORCH).** Implementa los grafos de decisión, la máquina de estados y la gestión de flujos lógicos del sistema multiagente. |

---

## 📂 Detalle de los Componentes

### 1. `01_analitica_pdf/`
*   **Propósito:** Extracción de texto y estructuración de datos desde documentos normativos complejos (PDFs del SENA).
*   **Archivos Clave:** `pdf_analyzer.py`, `patterns.yaml`.
*   **Valor Técnico:** Data Wrangling, parsing de documentos, preparación de corpus para bases vectoriales.

### 2. `02_pln_chat/`
*   **Propósito:** Motor de búsqueda semántica y generación de respuestas fundamentadas (RAG).
*   **Archivos Clave:** `embeddings.py`, `rag_engine.py`.
*   **Valor Técnico:** Uso de `SentenceTransformers`, similitud de coseno, integración con bases de datos vectoriales.

### 3. `03_vision_aprendices/`
*   **Propósito:** Procesamiento de imágenes institucionales, detección de objetos (YOLOv8) y clasificación.
*   **Archivos Clave:** `classifier.py`, `detector.py`.
*   **Valor Técnico:** Visión computacional, preprocesamiento de imágenes, alineación con la EU AI Act (privacidad).

### 4. `04_agentic_ai/`
*   **Propósito:** Lógica de orquestación para los agentes inteligentes del sistema FÉNIX.
*   **Archivos Clave:** `agent_orchestrator.py`.
*   **Valor Técnico:** Máquinas de estado, patrones de diseño multiagente, control de flujos de decisión autónomos.

---

## 🚀 Ejecución de los Módulos

*(Aquí puedes incluir los comandos para ejecutar cada módulo)*
```bash
# Ejemplo: Ejecutar la interfaz principal que integra los módulos
streamlit run app_master_inicio.py