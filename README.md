# 🤖 Master AI Portfolio: Enterprise Multi-Agent & MLOps Platform

[![Docker](https://img.shields.io/badge/Docker-29.9-blue?logo=docker)](https://www.docker.com/)[cite: 8, 10]
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-326CE5?logo=kubernetes)](https://kubernetes.io/)[cite: 8]
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python)](https://www.python.org/)[cite: 13, 14]
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-FF4B4B?logo=streamlit)](https://streamlit.io/)[cite: 15]
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql)](https://www.postgresql.org/)[cite: 12]

Repositorio profesional con la arquitectura integral, microservicios, pipelines de Data Engineering y modelos de Inteligencia Artificial desarrollados para el **Máster Universitario en Inteligencia Artificial (UNIR)**. La solución está diseñada bajo principios de código limpio (*Zero-Hardcode*), infraestructura contenerizada y manifiestos de despliegue orientados a entornos de producción Cloud-Native[cite: 8].

---

## 🏛️ Arquitectura de Software e Infraestructura

La plataforma opera mediante un esquema de **microservicios contenerizados y aislados**, permitiendo escalabilidad horizontal, alta disponibilidad y reproducibilidad en entornos multi-cloud (AWS / Azure)[cite: 8].

### 🛠️ Stack Tecnológico e Infraestructura

* **Core AI & ML:** LangGraph, Azure OpenAI, Scikit-Learn, Pandas, MLflow, ChromaDB.
* **Data Engineering:** PySpark, Apache Kafka, PostgreSQL.
* **Contenerización (OCI):** Construcción multicapa (*Multi-stage builds*) optimizada basada en `python:3.10-slim`[cite: 13, 14, 15].
* **Orquestación Local:** `Docker Compose` administrando aislamiento de red puente (*bridge network*) y volúmenes persistentes[cite: 8, 12].
* **Infraestructura como Código (IaC):** Manifiestos `Kubernetes` (`Deployment` y `Service`) declarativos en la carpeta `k8s/`[cite: 8].

---

## 🚀 Módulos del Portafolio

| Módulo | Descripción | Stack Técnico | Estado |
| :--- | :--- | :--- | :--- |
| **1. RAG SENA** | Buscador semántico y extracción analítica sobre documentación normativa en PDF. | FastAPI, ChromaDB, OpenAI, Docker | 🟢 Producción |
| **2. Tutor Inteligente** | Sistema conversacional multi-agente para orientación pedagógica personalizada. | LangGraph, Azure OpenAI, PostgreSQL | 🟢 Producción |
| **3. Data Engineering** | Pipeline de procesamiento y transmisión de datos a gran escala. | Apache Spark, Kafka, Docker | 🟢 Producción |
| **4. MLOps & Predicción** | Modelo supervisado de predicción de deserción con trazabilidad de experimentos. | Scikit-Learn, Pandas, MLflow | 🟢 Producción |
| **5. Sistema Multi-Agente** | Arquitectura avanzada de agentes autónomos con herramientas integradas. | LangGraph, MCP, Vector DB, K8s | 🟢 Producción |

---

## 💻 Guía de Despliegue y Ejecución

### Prerrequisitos
* **Docker Desktop** (versión 24.0+ con el motor de contenedores activo)[cite: 5, 8, 10].
* **Git**[cite: 8].

### 1. Clonar el repositorio
```bash
git clone [https://github.com/guzmantapiasjoseluis13-coder/master-ai-unir-portfolio.git](https://github.com/guzmantapiasjoseluis13-coder/master-ai-unir-portfolio.git)
cd master-ai-unir-portfolio