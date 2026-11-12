"""
Analítica Inteligente PDF — Módulo de Procesamiento Documental y Visión Artificial.
Asignatura: Procesamiento del Lenguaje Natural (PLN) & Visión Artificial (UNIR - 60 ECTS)
Autor: José Luis Guzmán Tapias
"""

import os
import re
import cv2
import numpy as np
import pypdf
import yaml
from typing import List, Dict, Any, Tuple, Optional
from pydantic import BaseModel, Field

# ==============================================================================
# MODELOS DE DATOS (PYDANTIC)
# ==============================================================================

class DatosInstitucionalesPDF(BaseModel):
    nombre_programa: str = Field(default="", description="Nombre del programa de formación")
    version: str = Field(default="1", description="Versión del diseño curricular")
    total_paginas: int = Field(default=0, description="Total de páginas del PDF")
    duracion_lectiva: str = Field(default="", description="Horas de etapa lectiva")
    duracion_productiva: str = Field(default="", description="Horas de etapa productiva")
    duracion_total: str = Field(default="", description="Horas totales del programa")
    perfiles_ocupacionales: List[str] = Field(default_factory=list, description="Lista de perfiles ocupacionales")

class DetalleCompetenciaPDF(BaseModel):
    nombre: str
    pagina_inicio: int
    pagina_fin: int
    texto_bloque: str

class TablasCurricularesPDF(BaseModel):
    resultados_aprendizaje: List[str] = Field(default_factory=list)
    conocimientos_proceso: List[str] = Field(default_factory=list)
    conocimientos_saber: List[str] = Field(default_factory=list)
    criterios_evaluacion: List[str] = Field(default_factory=list)

class MetricasPaginaPDF(BaseModel):
    ancho: int
    alto: int
    resolucion_aprox: str
    nivel_nitidez: float


# ==============================================================================
# CLASE PRINCIPAL DEL ANALIZADOR
# ==============================================================================

class AnalizadorPDFInteligente:
    """
    Motor de análisis de documentos curriculares no estructurados.
    Combina extracción de información mediante NLP con inspección de visión por computador.
    """

    def __init__(self, config_path: Optional[str] = None):
        self.config = self._cargar_configuracion(config_path)

    def _cargar_configuracion(self, config_path: Optional[str]) -> dict:
        if config_path and os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {
            "regex": {
                "version": r"Versi[oó]n[:\s]*(\d+)",
                "duracion_horas": r"\b(\d{3,4})\s*horas?\b",
                "limpieza_competencia": r"^(?:[0-9\.\-\s]+)"
            },
            "keywords": {
                "denominacion": ["DENOMINACIÓN", "DENOMINACION"],
                "ignorar_institucion": ["SENA"],
                "competencia_header": ["4.3", "NOMBRE DE LA COMPETENCIA"],
                "secciones_curriculares": {
                    "rap": ["4.5", "RESULTADO"],
                    "proceso": ["4.6.1", "PROCESO"],
                    "saber": ["4.6.2", "SABER"],
                    "criterios": ["4.7", "CRITERIOS"]
                }
            },
            "perfiles_candidatos": [
                "Cajeros de Servicios Financieros",
                "Auxiliares de servicios financieros",
                "Auxiliares de Información y Servicio al Cliente"
            ],
            "vision": {
                "clahe_clip_limit": 2.0,
                "clahe_grid_size": [8, 8],
                "canny_threshold1": 50,
                "canny_threshold2": 150
            }
        }

    def extraer_datos_institucionales(self, ruta_pdf: str) -> DatosInstitucionalesPDF:
        """Extrae metadatos institucionales del PDF usando PyPDF y Pydantic."""
        info = DatosInstitucionalesPDF()
        if not os.path.exists(ruta_pdf):
            return info

        reader = pypdf.PdfReader(ruta_pdf)
        info.total_paginas = len(reader.pages)
        if info.total_paginas == 0:
            return info

        # Texto acumulado de las primeras páginas
        texto_primeras = ""
        for i in range(min(5, info.total_paginas)):
            texto_primeras += f"\n--- PAGINA {i+1} ---\n" + (reader.pages[i].extract_text() or "")

        lineas_p1 = [l.strip() for l in (reader.pages[0].extract_text() or "").splitlines() if l.strip()]

        # Buscar nombre del programa
        denoms = self.config["keywords"]["denominacion"]
        for idx, linea in enumerate(lineas_p1):
            if any(kw in linea.upper() for kw in denoms):
                if ":" in linea and len(linea.split(":", 1)[1].strip()) > 3:
                    info.nombre_programa = linea.split(":", 1)[1].strip()
                    break
                elif idx + 1 < len(lineas_p1):
                    candidato = lineas_p1[idx + 1]
                    if len(candidato) > 3 and not any(ig in candidato.upper() for ig in self.config["keywords"]["ignorar_institucion"]):
                        info.nombre_programa = candidato
                        break

        # Buscar versión
        match_ver = re.search(self.config["regex"]["version"], texto_primeras, re.IGNORECASE)
        info.version = match_ver.group(1).strip() if match_ver else "1"

        # Buscar duración en horas
        matches_h = re.findall(self.config["regex"]["duracion_horas"], texto_primeras, re.IGNORECASE)
        if len(matches_h) >= 2:
            info.duracion_lectiva = f"{matches_h[0]} horas"
            prod_candidato = matches_h[1]
            if int(prod_candidato) > 1500 and len(matches_h) >= 3:
                prod_candidato = matches_h[2]
            info.duracion_productiva = f"{prod_candidato} horas"
            try:
                info.duracion_total = f"{int(matches_h[0]) + int(prod_candidato)} horas"
            except Exception:
                pass

        # Perfiles ocupacionales en página 2
        if info.total_paginas >= 2:
            texto_pag2 = (reader.pages[1].extract_text() or "").lower()
            for cargo in self.config["perfiles_candidatos"]:
                if cargo.lower() in texto_pag2 and cargo not in info.perfiles_ocupacionales:
                    info.perfiles_ocupacionales.append(cargo)

        return info

    def compilar_dom_competencias(self, ruta_pdf: str) -> Dict[str, DetalleCompetenciaPDF]:
        """Compila las competencias encontradas estructurando un Modelo DOM."""
        competencias_dom: Dict[str, DetalleCompetenciaPDF] = {}
        if not os.path.exists(ruta_pdf):
            return competencias_dom

        reader = pypdf.PdfReader(ruta_pdf)
        lista_comp = []

        headers = self.config["keywords"]["competencia_header"]
        for i, page in enumerate(reader.pages):
            texto_pag = page.extract_text() or ""
            lineas = [l.strip() for l in texto_pag.splitlines() if l.strip()]

            for idx, linea in enumerate(lineas):
                if any(h in linea.upper() for h in headers):
                    nombre_hallado = ""
                    if ":" in linea:
                        candidato = linea.split(":", 1)[1].strip()
                        if len(candidato) > 8 and not any(h in candidato for h in headers):
                            nombre_hallado = candidato

                    if not nombre_hallado:
                        for offset in [1, 2, 3]:
                            if idx + offset < len(lineas):
                                sig = lineas[idx + offset]
                                if len(sig) > 12:
                                    nombre_hallado = sig
                                    break

                    if nombre_hallado and len(nombre_hallado) > 10:
                        c_limpio = re.sub(self.config["regex"]["limpieza_competencia"], "", nombre_hallado).strip(" :.-")
                        if len(c_limpio) > 10 and c_limpio.upper() not in [c["nombre"] for c in lista_comp]:
                            lista_comp.append({
                                "nombre": c_limpio.upper(),
                                "pagina_inicio": i + 1,
                                "pagina_fin": i + 1,
                                "texto_bloque": texto_pag
                            })

        for idx, comp in enumerate(lista_comp, start=1):
            key = f"{idx:02d}. {comp['nombre']}"
            competencias_dom[key] = DetalleCompetenciaPDF(**comp)

        return competencias_dom

    def extraer_tablas_desde_dom(self, texto_bloque: str) -> TablasCurricularesPDF:
        """Categoriza RAP, Procesos, Saberes y Criterios a partir de un bloque de texto."""
        tablas = TablasCurricularesPDF()
        seccion_activa = None
        kw_sec = self.config["keywords"]["secciones_curriculares"]

        for linea in texto_bloque.splitlines():
            l_trim = linea.strip()
            if not l_trim or len(l_trim) < 2:
                continue
            l_upper = l_trim.upper()

            if all(k in l_upper for k in kw_sec["rap"]):
                seccion_activa = "RAP"
                continue
            elif any(k in l_upper for k in kw_sec["proceso"]):
                seccion_activa = "PROCESO"
                continue
            elif any(k in l_upper for k in kw_sec["saber"]):
                seccion_activa = "SABER"
                continue
            elif any(k in l_upper for k in kw_sec["criterios"]):
                seccion_activa = "CRITERIOS"
                continue

            if seccion_activa == "RAP":
                tablas.resultados_aprendizaje.append(l_trim)
            elif seccion_activa == "PROCESO":
                tablas.conocimientos_proceso.append(l_trim)
            elif seccion_activa == "SABER":
                tablas.conocimientos_saber.append(l_trim)
            elif seccion_activa == "CRITERIOS":
                tablas.criterios_evaluacion.append(l_trim)

        return tablas

    def analizar_pagina_pdf(self, img_bgr: np.ndarray) -> Tuple[np.ndarray, MetricasPaginaPDF]:
        """Aplica filtros de Visión Artificial y calcula métricas de calidad de imagen."""
        gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        clip_limit = self.config["vision"]["clahe_clip_limit"]
        grid = tuple(self.config["vision"]["clahe_grid_size"])

        clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=grid)
        gray_clahe = clahe.apply(gray)

        c_th1 = self.config["vision"]["canny_threshold1"]
        c_th2 = self.config["vision"]["canny_threshold2"]
        canny = cv2.Canny(gray_clahe, c_th1, c_th2)
        canny_rgb = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)

        h, w = img_bgr.shape[:2]
        metricas = MetricasPaginaPDF(
            ancho=w,
            alto=h,
            resolucion_aprox=f"{w}x{h} px",
            nivel_nitidez=float(cv2.Laplacian(gray, cv2.CV_64F).var())
        )
        return canny_rgb, metricas
