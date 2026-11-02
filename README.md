# 🤖 Master AI Portfolio: Enterprise Multi-Agent & MLOps Platform

[![Docker OCI](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)[cite: 8, 10]
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Orchestration-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io/)[cite: 8]
[![Python 3.10](https://img.shields.io/badge/Python-3.10%20%7C%20FastAPI-3776AB?logo=python&logoColor=white)](https://www.python.org/)[cite: 13, 14]
[![Streamlit](https://img.shields.io/badge/Streamlit-Enterprise%20UI-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)[cite: 15]
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%20Alpine-4169E1?logo=postgresql&logoColor=white)](https://www.postgresql.org/)[cite: 12]
[![MLflow](https://img.shields.io/badge/MLflow-Experiment%20Tracking-0175C2?logo=mlflow&logoColor=white)](https://mlflow.org/)

Repositorio de ingeniería avanzada e inteligencia artificial desarrollado como culminación del **Máster Universitario en Inteligencia Artificial (UNIR)**. Diseñado bajo rigurosos estándares de la industria tecnológica europea, este portafolio implementa soluciones *Production-Ready*, arquitectura limpia, microservicios desacoplados y prácticas estrictas de MLOps y DevOps.

---

## 📑 Tabla de Contenidos

1. [Arquitectura de Software e Infraestructura](#-arquitectura-de-software-e-infraestructura)
2. [Matriz de Microservicios y Módulos](#-matriz-de-microservicios-y-módulos)
3. [Stack Tecnológico y Patrones de Diseño](#-stack-tecnológico-y-patrones-de-diseño)
4. [Guía de Despliegue y Ejecución Local](#-guía-de-despliegue-y-ejecución)
5. [Infraestructura como Código (Kubernetes)](#-infraestructura-como-código-iac)
6. [Autoría y Contexto Académico](#-autoría)

---

## 🏛️ Arquitectura de Software e Infraestructura

La plataforma se estructura mediante un diseño modular desacoplado. Los servicios se comunican a través de redes internas seguras (*bridge networks*) con persistencia de datos administrada mediante volúmenes OCI.

```text
                               +-----------------------------+
                               |     Ingress / Load Balancer |
                               +--------------+--------------+
                                              |
                                              v
                              +---------------+---------------+
                              |   Docker Compose / Kubernetes  |
                              +---------------+---------------+
                                              |
                     +------------------------+------------------------+
                     |                                                 |
                     v                                                 v
      +--------------+--------------+                   +--------------+--------------+
      |  Frontend / AI Core Service |                   |   Stateful Database Service |
      |   (Streamlit + FastAPI)     | <--- Internal --> |    (PostgreSQL 15 Alpine)    |
      |        Port: 8501           |     Network       |          Port: 5432         |
      +-----------------------------+                   +-----------------------------+