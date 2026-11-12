# 🔥 Proyecto FÉNIX — Núcleo Científico y Técnico (TFM)

![Status](https://img.shields.io/badge/Status-Research_%26_Development-orange?style=for-the-badge)
![UNIR](https://img.shields.io/badge/UNIR-Master_AI-blue?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Multi--Agent_%2B_ORCH-purple?style=for-the-badge)

Bienvenido al núcleo del **Proyecto FÉNIX**, el Trabajo Fin de Máster (TFM) para el **Máster Universitario en Inteligencia Artificial de la UNIR**.

Este directorio contiene la totalidad del ecosistema del proyecto: desde la fundamentación científica y los protocolos experimentales hasta la implementación del sistema multiagente (Backend y Frontend) que servirá para validar empíricamente las hipótesis de la investigación.

---

## 🎯 1. Resumen Ejecutivo del TFM

**Problema Científico:** Insuficiente especificación y evaluación experimental de arquitecturas inteligentes multiagente orientadas a la Formación Profesional Integral (SENA).
**Solución Propuesta:** FÉNIX, una arquitectura gobernada por un Orquestador (ORCH) que coordina dos Capacidades Inteligentes Especializadas (CIE-01: Diseño Didáctico y CIE-02: Tutoría).
**Enfoque Metodológico:** Investigación aplicada con diseño experimental comparativo (Condición A: Asistente General vs. Condición B: Arquitectura FÉNIX).

---

## 🏗️ 2. Arquitectura del Sistema Implementado

La carpeta `tfm/` contiene el código fuente funcional que materializa la arquitectura teórica. Está diseñada bajo un patrón de microservicios desacoplados:

```text
tfm/
├── backend_api/       # El "Cerebro" (FastAPI + Lógica de Agentes)
│   ├── analitica_pdf/ # SKILL: Extracción documental
│   ├── pln_chat/      # SKILL: RAG y búsqueda semántica
│   └── vision_aprendices/ # SKILL: Procesamiento de imágenes
│
├── frontend_streamlit/ # La "Cara" (Interfaz de usuario)
│   └── pages/         # Módulos interactivos de validación
│
└── docs/              # (Próximamente) Repositorio documental R00-R13