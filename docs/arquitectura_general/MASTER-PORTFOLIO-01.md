# ⚙️ MASTER-PORTFOLIO-01: Estándar de Ingeniería, Calidad y Reproducibilidad del Portafolio de IA

> **Identificador:** MASTER-PORTFOLIO-01  
> **Nombre del Repositorio:** master_ai_unir_portafolio  
> **Tipo de Documento:** Estándar técnico, guía de calidad de software y directrices de reproducibilidad  
> **Versión:** 1.0 (Versión fundacional operativa)  
> **Documento Relacionado:** [MASTER-PORTFOLIO-00: Carta Fundacional y Arquitectura Maestra](MASTER-PORTFOLIO-00.md)  
> **Ubicación:** `docs/arquitectura_general/MASTER-PORTFOLIO-01.md`  
> **Responsable:** José Luis Guzmán Tapias  
> **Programa Académico:** Maestría Universitaria en Inteligencia Artificial — UNIR  
> **Ámbito de Aplicación:** Todos los submódulos, experimentos, proyectos y TFM del repositorio  

---

## 📋 Control Documental

### Historial de Versiones

| Versión | Fecha | Descripción |
| :--- | :--- | :--- |
| **1.0** | Noviembre de 2026 | Formulación del estándar de ingeniería, calidad, CI/CD, pruebas y reproducibilidad |

### Propósito del Documento

El presente documento establece los estándares técnicos, metodológicos y de calidad que orientarán el desarrollo, mantenimiento y evolución del repositorio `master_ai_unir_portafolio`.

Su propósito es garantizar que los ejercicios académicos, experimentos, investigaciones, publicaciones, laboratorios y proyectos aplicados se desarrollen bajo criterios coherentes de ingeniería de software, reproducibilidad, seguridad, trazabilidad y documentación.

El portafolio no se construirá únicamente para almacenar código. Se concibe como un entorno de trabajo profesional en el que cada resultado técnico debe poder comprenderse, ejecutarse, verificarse y, cuando corresponda, reproducirse.

Por tanto, cada proyecto deberá procurar responder cinco preguntas clave:
1. **¿Qué problema aborda?**
2. **¿Qué metodología y herramientas utiliza?**
3. **¿Cómo se desarrolló?**
4. **¿Cómo se comprueba que funciona?**
5. **¿Qué evidencia permite verificar sus resultados?**

Este estándar será aplicable a los siete dominios definidos en `MASTER-PORTFOLIO-00`, respetando las características particulares de cada uno.

---

## 1. 🎯 Objetivos

### 1.1. Objetivo General
Definir un marco común de ingeniería, calidad y reproducibilidad que permita desarrollar un portafolio de inteligencia artificial técnicamente consistente, documentado, seguro y verificable.

### 1.2. Objetivos Específicos
* Establecer convenciones de organización y desarrollo del código.
* Definir criterios para la gestión de dependencias y entornos aislados.
* Establecer prácticas de pruebas automatizadas y validación de resultados.
* Normalizar la documentación técnica y científica.
* Incorporar mecanismos de integración continua (CI/CD) con responsabilidades delimitadas.
* Establecer criterios de seguridad y protección de información privada/sensible.
* Definir estrategias para gestionar datos, modelos y artefactos pesados.
* Facilitar la ejecución y reproducción de experimentos de IA.
* Mantener trazabilidad entre requisitos, código, pruebas y resultados.
* Promover prácticas compatibles con entornos profesionales de desarrollo de IA en España y la UE.

---

## 2. ⚖️ Principios de Ingeniería

1. **Reproducibilidad:** Registrar versiones de Python, dependencias, entornos, parámetros, semillas aleatorias, datos de entrada y limitaciones conocidas.
2. **Trazabilidad:** Vincular cada resultado relevante con su origen (problema, requisito, diseño, código, prueba y conclusión).
3. **Calidad Verificable:** Exigir pruebas estáticas y dinámicas apropiadas según la complejidad del proyecto.
4. **Seguridad desde el Diseño:** Proteger credenciales, datos personales de aprendices y recursos institucionales desde la primera línea de código.
5. **Simplicidad y Mantenibilidad:** Evitar dependencias o arquitecturas innecesarias que no aporten valor técnico real.
6. **Honestidad Técnica y Científica:** Distinguir claramente entre ejercicio académico, prototipo, experimento, solución desplegada y resultado validado.

---

## 3. 🏗️ Estándar de Organización del Código

### 3.1. Convenciones Generales
* Nombres de archivos y directorios en minúsculas en formato `snake_case`.
* Funciones cortas con una sola responsabilidad bien definida.
* Separación clara entre configuración, lógica de negocio, datos e interfaz de presentación.

### 3.2. Estructura de Referencia para Proyectos Python

```text
nombre_proyecto/
│
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
│
├── docs/
│   ├── arquitectura.md
│   ├── metodologia.md
│   └── decisiones_tecnicas.md
│
├── src/
│   └── nombre_proyecto/
│       ├── __init__.py
│       ├── config.py
│       ├── main.py
│       └── ...
│
├── tests/
│   ├── test_config.py
│   └── ...
│
├── scripts/
│
├── data/
│   ├── README.md
│   ├── raw/
│   ├── processed/
│   └── external/
│
└── outputs/
    └── README.md
```
---

## 11. 🐳 Contenedores y Reproducibilidad del Entorno

### 11.1. Uso de Docker
Docker se utilizará para empaquetar aplicaciones y garantizar entornos de ejecución idénticos entre desarrollo y producción. Se incorporará prioritariamente en APIs, microservicios, frontend y sistemas multiagente.

### 11.2. Orquestación con `docker-compose.yml`
Se utilizará para coordinar arquitecturas multi-servicio (e.g., Backend FastAPI + Base de Datos Vectorial + UI Streamlit).

### 11.3. Seguridad de Contenedores
Las imágenes utilizarán configuraciones livianas (`python:3.11-slim`), evitarán secretos incrustados en capas y se ejecutarán bajo usuarios sin privilegios elevables.

---

## 12. 🛡️ Seguridad y Protección de Información

### 12.1. Credenciales y Secretos
Las claves API, tokens y credenciales se gestionarán estrictamente mediante variables de entorno local (`.env`) pasadas en tiempo de ejecución. Prohibido incluir valores reales en el código fuente.

### 12.2. Plantilla Externa (`.env.example`)
Se conservará una plantilla `.env.example` con los nombres de las variables requeridas y valores ilustrativos no sensibles.

### 12.3. Auditoría Previas a Publicar
Antes de integrar cambios a ramas públicas, se verificará que el historial de Git y los commits no contengan tokens, datos personales ni información confidencial institucional.

### 12.4. Licencias y Propiedad Intelectual
Se documentarán explícitamente las licencias de datasets, modelos y código reutilizado, respetando los derechos de autor de terceros.

---

## 13. 🔀 Control de Versiones y Colaboración

### 13.1. Git y Commits Descriptivos
Los commits deben representar unidades de trabajo comprensibles usando prefijos claros:
* `docs:` Cambios en documentación.
* `feat:` Nuevas funcionalidades o módulos.
* `fix:` Corrección de errores.
* `test:` Adición o modificación de pruebas.
* `refactor:` Mejoras de código sin cambiar funcionalidad.

### 13.2. Estrategia de Ramas
* `main`: Versión estable y de producción.
* Ramas de trabajo (`feature/`, `fix/`, `docs/`): Desarrollos en curso antes de integrarse mediante revisión.

---

## 14. 🧪 Reproducibilidad de Experimentos de IA

Los experimentos con modelos generativos, NLP y Computer Vision registrarán explícitamente:
* Identificador único de sesión.
* Proveedor, modelo exacto y parámetros (temperatura, top_p, max_tokens).
* Versión exacta de prompts y datasets de prueba.
* Semillas aleatorias (`seed`) cuando la herramienta lo permita.
* Fecha de ejecución y métricas obtenidas.

---

## 15. 📊 Criterios de Calidad por Tipo de Proyecto

| Tipo de Trabajo | Evidencia Mínima Esperada |
| :--- | :--- |
| **Ejercicio Académico** | Código limpio, explicación clara e instrucciones de ejecución. |
| **Laboratorio Técnico** | Procedimiento, configuración de entorno y métricas registradas. |
| **Experimento de IA** | Diseño, datos, hiperparámetros, resultados y limitaciones. |
| **Proyecto Aplicado** | Requisitos, arquitectura, pruebas automatizadas y demostración. |
| **Investigación** | Pregunta, metodología, evidencia, discusión y limitaciones. |
| **Sistema Desplegado** | Guías de operación, empaquetado Docker y observabilidad. |

---

## 16. 📈 Indicadores de Seguimiento (KPIs)

* Porcentaje de proyectos con suite de `pytest` funcional.
* Ausencia absoluta de credenciales y datos privados en el historial de Git.
* Porcentaje de subproyectos con ficha `README.md` completa (9 preguntas).
* Nivel de cobertura de pruebas en módulos de producción.

---

## 17. 📶 Aplicación Progresiva del Estándar

El estándar se aplicará por niveles de madurez técnica:
* **Nivel 1 — Fundacional:** Estructura limpia, README, dependencias declaradas e instrucciones de ejecución.
* **Nivel 2 — Verificable:** Pruebas automatizadas básicas, linters e historial Git limpio.
* **Nivel 3 — Reproducible:** Entornos controlados, configuración documentada y versionado de artefactos.
* **Nivel 4 — Profesional:** Integración continua funcional, Docker, seguridad automatizada y observabilidad.

---

## 18. 🔗 Relación con los Dominios del Portafolio

Este estándar aplica a los 7 dominios de `MASTER-PORTFOLIO-00`[cite: 7]:
* **01_formacion_academica:** Organización de entregas universitarias.
* **02_investigacion:** Trazabilidad metodológica.
* **03_publicaciones:** Licencias y control de versiones de manuscritos.
* **04_laboratorio_ia:** Registro estricto de experimentos.
* **05_proyectos:** Fichas completas, tests y Docker.
* **06_tfm_proyecto_fenix:** Rigor científico y de ingeniería avanzado.
* **07_portafolio_profesional:** Casos de estudio y evidencias de empleabilidad.

---

## 19. 🦅 Relación con Proyecto FÉNIX

Proyecto FÉNIX adopta este estándar como su norma de ingeniería. Las pruebas técnicas deben estar vinculadas a las hipótesis científicas, preservando la confidencialidad de la información y evitando presentar prototipos como validaciones científicas sin evaluación metodológica.

---

## 20. ⚙️ Gobierno y Mantenimiento del Estándar

Toda modificación relevante a este documento deberá ser justificada, mantener estricta coherencia con `MASTER-PORTFOLIO-00`[cite: 7] e incrementar la versión del control documental.

---

## 21. 📌 Decisiones Pendientes de Implementación

Las siguientes decisiones se formalizarán mediante Registros de Decisiones Arquitectónicas (ADR):
* Selección definitiva del gestor de dependencias (`uv`, `poetry` o `pip-tools`).
* Versión exacta de Python por subproyecto.
* Configuración específica de `ruff` / `pytest`.
* Definición de workflows en GitHub Actions.

---

## 22. ✅ Criterios de Aprobación

Este documento se aprueba formalmente al establecer normas claras de calidad, reproducibilidad y seguridad que pueden ser aplicadas de forma progresiva sin imponer barreras innecesarias.

---

## 23. 🌟 Declaración Final

> *La calidad profesional de un proyecto de inteligencia artificial no se demuestra únicamente por el modelo utilizado o por el código producido, sino por la capacidad de explicar, justificar, ejecutar, verificar y reproducir el trabajo realizado.*

**MASTER AI UNIR — AI Research & Engineering Portfolio**  
*Formación rigurosa. Investigación aplicada. Ingeniería reproducible. Conocimiento verificable[cite: 9].*

---
*Fin del documento MASTER-PORTFOLIO-01 — Versión 1.0[cite: 9].*