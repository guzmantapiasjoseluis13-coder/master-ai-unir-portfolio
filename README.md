# 🦅 Master AI Enterprise Portafolio | UNIR & Vision Fénix AI

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/) [![Streamlit](https://img.shields.io/badge/streamlit-1.35%2B-red.svg)](https://streamlit.io/) [![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-orange.svg)](https://pytorch.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Plataforma Enterprise de Visión Artificial, Analítica Documental y Sistemas Cognitivos desarrollada como parte de las actividades prácticas y Trabajo de Fin de Máster (TFM) del **Máster Universitario en Inteligencia Artificial** de la **Universidad Internacional de La Rioja (UNIR)**.


## 🏛️ Contexto Académico e Institucional

- **Institución:** Universidad Internacional de La Rioja (UNIR) — Sede Central (Logroño, España) y Delegación (Bogotá, Colombia).

- **Programa:** Máster Universitario en Inteligencia Artificial (60 ECTS).

- **Asignatura Base:** Visión Artificial (6 ECTS).

- **Entorno de Aplicación Práctica:** SENA Antioquia (Medellín, Colombia).


## 🚀 Arquitectura del Sistema (Multipágina)

El monorepo está estructurado bajo principios de diseño limpio, modularidad y ausencia total de código quemado (*zero-hardcoding*):

```
master\_ai\_unir\_portafolio/  
├── app\_master\_inicio.py                 \# 🚀 Lanzador Maestro (Historia UNIR, Plan de Estudios y Perfil)  
├── requirements.txt                     \# Dependencias científicas estandarizadas  
├── data/  
│   └── raw/  
│       ├── oferta\_medellin.txt          \# Base RAG institucional  
│       └── documentos\_pdf/              \# Normativa académica en PDF  
├── src/  
│   ├── vision\_uniformes/                \# Módulo 1: Auditoría de Uniformes, ROI, OCR y Mapas 3D  
│   └── analitica\_pdf/                   \# Módulo 2: Parser y Extracción de Competencias PDF  
└── pages/  
    ├── 1\_🦅\_Vision\_Fenix\_SENA.py         \# Vista interactiva de auditoría óptica  
    └── 2\_📄\_Parser\_Competencias\_PDF.py   \# Analítica de documentos institucionales
```

