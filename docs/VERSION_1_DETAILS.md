# 📑 Technical Design Document (TDD): Motor Determinista de Extracción Espacial por Coordenadas (`PyMuPDF`)

- **Autor:** Jose Luis Guzman Tapias 

- **Contexto Académico & Profesional:** Máster Universitario en Inteligencia Artificial | Arquitectura de Sistemas de Procesamiento Documental 

- **Versión del Módulo:** v1.0.0 (Baseline Determinista)

- **Dominio:** Procesamiento Automático de Documentos (Document Intelligence) aplicado a Normativa Institucional SENA.


## 1. Executive Summary & Problem Statement

En el ecosistema de la educación vocacional e institucional (SENA), los diseños curriculares son publicados en formatos PDF no estructurados o semi-estructurados con maquetaciones visuales complejas (tablas de portada, metadatos en celdas y bloques multilínea). 

Las aproximaciones tradicionales basadas en la extracción de texto plano en crudo (*Raw Text Streaming*) colapsan debido al orden arbitrario de lectura de los streams de los PDFs. El objetivo de este módulo (**Versión 1**) es diseñar un **parser heurístico determinista** basado en la geometría espacial de los documentos, utilizando cajas delimitadoras (*Bounding Boxes*) para resolver la ambigüedad posicional de las etiquetas sin intervención manual ni dependencias de modelos de lenguaje pesados.


## 2. System Architecture & Core Mechanics (Rule-Based Parsing)

La arquitectura de la Versión 1 implementa un pipeline determinista dividido en tres fases secuenciales:

```
`\[ PDF Directory: data/raw/ \] `

`        │`

`        ▼ (PyMuPDF / fitz stream)`

`\[ Spatial Bounding Box Extraction (x0, y0, x1, y1) \]`

`        │`

`        ▼ (Horizontal Band Clustering)`

`\[ Proximity-Based Key-Value Association \]`

`        │`

`        ▼ (Deterministic Normalization & RegEx)`

`\[ Structured Metadata Dictionary -\> Markdown Output Engine \]`
```

### A. Extracción de Coordenadas Espaciales (Spatial Tokenization)

A diferencia de los extractores convencionales, el motor utiliza la API de bajo nivel de PyMuPDF para recuperar tuplas de palabras con sus respectivas coordenadas geométricas:

$$\\text\{Word Token\} = (x\_0, y\_0, x\_1, y\_1, \\text\{text\}, \\text\{block\}, \\text\{line\}, \\text\{word\\\_no\})$$


### B. Algoritmo de Proximidad Horizontal (Spatial Proximity Matching)

Para asociar una etiqueta institucional (ej. *"Denominación del Programa"*, *"Código"*, *"Etapa Lectiva"*) con su respectivo valor tabular ubicado a la derecha, se implementa una función de proximidad geométrica en el eje horizontal ($x$) y bandas de tolerancia vertical ($y$):

- **Tolerancia Vertical ($\\Delta y \< 10\\text\{px\}$):** Agrupa tokens dentro de la misma línea horizontal visual.

- **Filtro Direccional ($x \> x\_\{\\text\{target\}\}$):** Captura exclusivamente el contenido ubicado en la celda contigua derecha, aislando ruido de encabezados o pies de página.


## 3. Tech Stack & Engineering Standards

- **Lenguaje:** Python 3.10+ (Tipado estático mediante `typing` para mantenibilidad a escala).

- **PDF Processing Engine:** `PyMuPDF` (`fitz`) por su alto rendimiento en la renderización y acceso a flujos vectoriales y geométricos.

- **Normalización:** Expresiones Regulares avanzadas (`re`) para el aislamiento estricto de códigos institucionales de 6 dígitos y versiones numéricas.

- **Interface Layer:** Streamlit (Patrón de visualización reactiva).


## 4. Production-Grade Code Implementation (`rag\_engine\_v1.py`)


Python

```
`\# flake8: noqa: E203, E501`

`import os`

`import re`

`import fitz  \# PyMuPDF`

`from typing import List, Dict, Any`



`class ProfessionalSenaRAGV1:`

`    """`

`    Motor RAG Determinista (Baseline) basado en análisis de geometría espacial `

`    de coordenadas y proximidad horizontal para parsing de diseños curriculares.`

`    """`


`    def \_\_init\_\_(self, directorio\_raw: str = "data/raw") -\> None:`

`        self.directorio\_raw = directorio\_raw`

`        self.programas\_metadata: List\[Dict\[str, Any\]\] = \[\]`

`        self.\_indexar\_base\_documental()`


`    def \_indexar\_base\_documental(self) -\> None:`

`        """Escanea el repositorio documental y extrae metadatos de la Pág. 1 por coordenadas."""`

`        if not os.path.exists(self.directorio\_raw):`

`            return`


`        archivos = os.listdir(self.directorio\_raw)`

`        pdfs = \[f for f in archivos if f.lower().endswith(".pdf")\]`


`        for pdf\_file in pdfs:`

`            ruta\_pdf = os.path.join(self.directorio\_raw, pdf\_file)`

`            try:`

`                doc: Any = fitz.open(ruta\_pdf)`

`                if len(doc) == 0:`

`                    continue`


`                meta = self.\_parsear\_por\_coordenadas(pdf\_file, doc\[0\])`

`                self.programas\_metadata.append(meta)`

`                doc.close()`

`            except Exception:`

`                pass`


`    def \_parsear\_por\_coordenadas(self, pdf\_file: str, page: Any) -\> Dict\[str, Any\]:`

`        """Implementa el algoritmo de proximidad espacial (Bounding Box Mapping)."""`

`        denominacion = "No especificado"`

`        codigo = "N/A"`

`        version = "1"`

`        lectiva = "No especificado"`

`        productiva = "No especificado"`

`        tipo\_programa = "No especificado"`

`        titulo\_certificado = "No especificado"`


`        try:`

`            \# Extracción de tokens con coordenadas espaciales (x0, y0, x1, y1)`

`            words = page.get\_text("words")`


`            def buscar\_valor(etiquetas: List\[str\]) -\> str:`

`                for w in words:`

`                    w\_text = w\[4\].lower()`

`                    if any(etik in w\_text for etik in etiquetas):`

`                        y\_target = w\[1\]`

`                        x\_target = w\[2\]`

`                        \# Filtrado espacial: misma línea horizontal (tolerancia 10px) y hacia la derecha`

`                        candidatos = \[`

`                            ww\[4\] for ww in words `

`                            if abs(ww\[1\] - y\_target) \< 10 and ww\[0\] \> x\_target - 5`

`                        \]`

`                        if candidatos:`

`                            filtrados = \[`

`                                c for c in candidatos `

`                                if not any(e in c.lower() for e in etiquetas) and not c.startswith("1.")`

`                            \]`

`                            if filtrados:`

`                                return " ".join(filtrados).strip()`

`                return "No especificado"`


`            \# Mapeo determinista por proximidad de etiquetas`

`            den\_val = buscar\_valor(\["denominación", "denominacion"\])`

`            if den\_val != "No especificado" and "vigente" not in den\_val.lower():`

`                denominacion = den\_val`


`            cod\_val = buscar\_valor(\["código", "codigo"\])`

`            if cod\_val != "No especificado":`

`                m\_c = re.search(r"\\b(\\d\{5,6\})\\b", cod\_val)`

`                if m\_c:`

`                    codigo = m\_c.group(1)`


`            ver\_val = buscar\_valor(\["versión", "version"\])`

`            if ver\_val != "No especificado":`

`                m\_v = re.search(r"\\b(\\d\{1,2\})\\b", ver\_val)`

`                if m\_v:`

`                    version = m\_v.group(1)`


`            lectiva = buscar\_valor(\["lectiva"\])`

`            productiva = buscar\_valor(\["productiva"\])`

`            tipo\_programa = buscar\_valor(\["tipo"\])`

`            titulo\_certificado = buscar\_valor(\["título", "titulo", "certificado"\])`


`            \# Fallback global por RegEx en caso de divergencia geométrica`

`            if codigo == "N/A":`

`                full\_txt = " ".join(\[w\[4\] for w in words\])`

`                m\_all = re.search(r"\\b(\\d\{6\})\\b", full\_txt)`

`                if m\_all:`

`                    codigo = m\_all.group(1)`


`        except Exception:`

`            pass`


`        return \{`

`            "archivo": pdf\_file,`

`            "codigo": codigo,`

`            "denominacion": denominacion,`

`            "version": version,`

`            "lectiva": lectiva,`

`            "productiva": productiva,`

`            "tipo\_programa": tipo\_programa,`

`            "titulo\_certificado": titulo\_certificado,`

`        \}`


`    def consultar(self, query: str) -\> str:`

`        """Motor de consulta indexada por código institucional."""`

`        query\_clean = query.strip()`

`        query\_lower = query\_clean.lower()`


`        if any(s in query\_lower for s in \["hola", "buenos dias", "buenas tardes", "saludos"\]):`

`            return (`

`                f"¡Hola! 👋 Indexados \*\*\{len(self.programas\_metadata)\} diseños curriculares\*\* "`

`                f"mediante el motor heurístico determinista (Versión 1)."`

`            )`


`        numeros = re.findall(r"\\b\\d\{5,6\}\\b", query)`

`        if numeros:`

`            codigo\_buscado = numeros\[0\]`

`            for meta in self.programas\_metadata:`

`                if meta\["codigo"\] == codigo\_buscado:`

`                    return self.\_formatear\_respuesta(meta, query\_clean)`


`        return f"❌ No se encontró ningún diseño curricular asociado al código: \*\*\{query\_clean\}\*\*."`


`    def \_formatear\_respuesta(self, meta: Dict\[str, Any\], query: str) -\> str:`

`        q\_lower = query.lower()`

`        filas = \[`

`            f"| \*\*Nombre del Programa de Formación\*\* | \*\*\{meta\['denominacion'\]\}\*\* |",`

`            f"| \*\*Código\*\* | \`\{meta\['codigo'\]\}\` |",`

`            f"| \*\*Versión\*\* | \{meta\['version'\]\} |",`

`        \]`


`        if "lectiva" in q\_lower or "hora" in q\_lower:`

`            filas.append(f"| \*\*Horas Etapa Lectiva\*\* | \{meta\['lectiva'\]\} |")`

`        if "productiva" in q\_lower or "hora" in q\_lower:`

`            filas.append(f"| \*\*Horas Etapa Productiva\*\* | \{meta\['productiva'\]\} |")`

`        if "tipo" in q\_lower:`

`            filas.append(f"| \*\*Tipo de Programa\*\* | \{meta\['tipo\_programa'\]\} |")`

`        if "título" in q\_lower or "titulo" in q\_lower or "certificado" in q\_lower or "obtendrá" in q\_lower:`

`            filas.append(f"| \*\*Título o Certificado\*\* | \{meta\['titulo\_certificado'\]\} |")`


`        return (`

`            f"\#\#\# 📋 Resultado Analítico (Versión 1 - Baseline Determinista)\\n\\n"`

`            f"\*\*Consulta:\*\* \_\{query\}\_\\n\\n"`

`            f"| Métrica / Campo | Valor Extraído |\\n"`

`            f"| :--- | :--- |\\n"`

`            f"\{'\\n'.join(filas)\}\\n"`

`        )`
```


## 5. Limitaciones Arquitectónicas (Justificación hacia la Versión 2)

A pesar de la alta eficiencia computacional y el consumo cero de tokens de LLM de esta versión, el enfoque determinista presenta vulnerabilidades inherentes que motivan la evolución del proyecto:

1. **Sensibilidad al Layout:** Modificaciones menores en la plantilla del PDF (cambios en coordenadas de celdas o saltos de línea imprevistos) rompen las reglas de proximidad geométrica.

2. **Falta de Razonamiento Semántico:** No es capaz de interpretar consultas complejas o multilingües que no coincidan estrictamente con las etiquetas lógicas predefinidas.

