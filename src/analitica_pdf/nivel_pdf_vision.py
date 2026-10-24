# flake8: noqa: E203, E501
import os
import re
import cv2
import numpy as np
import fitz  # PyMuPDF
from typing import List, Dict, Any, Tuple


def rasterizar_pdf_a_imagenes(ruta_pdf: str, dpi: int = 150) -> List[np.ndarray]:
    """Convierte cada página del PDF en una matriz numpy BGR."""
    imagenes_bgr = []
    if not os.path.exists(ruta_pdf):
        return imagenes_bgr

    doc: fitz.Document = fitz.open(ruta_pdf)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)

    for pagina in doc:
        pix = pagina.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        arr = np.frombuffer(img_bytes, dtype=np.uint8)
        img_bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
        if img_bgr is not None:
            imagenes_bgr.append(img_bgr)

    doc.close()
    return imagenes_bgr


def extraer_datos_institucionales(ruta_pdf: str) -> Dict[str, Any]:
    """Extrae metadatos y perfiles ocupacionales del PDF[cite: 13]."""
    info = {
        "nombre_programa": "",
        "version": "",
        "total_paginas": 0,
        "duracion_lectiva": "",
        "duracion_productiva": "",
        "duracion_total": "",
        "perfiles_ocupacionales": [],
    }
    if not os.path.exists(ruta_pdf):
        return info

    doc: fitz.Document = fitz.open(ruta_pdf)
    info["total_paginas"] = len(doc)

    pagina_1 = doc[0]
    raw_blocks = pagina_1.get_text("blocks")
    blocks: List[Any] = list(raw_blocks) if isinstance(raw_blocks, list) else []
    blocks.sort(key=lambda b: (round(b[1] / 15), round(b[0] / 50)))
    bloques_p1 = [str(b[4]).strip() for b in blocks if len(b) > 4 and str(b[4]).strip()]

    texto_primeras = ""
    for i in range(min(5, len(doc))):
        texto_primeras += f"\n--- PAGINA {i+1} ---\n" + str(doc[i].get_text("text"))

    for idx, bloque in enumerate(bloques_p1):
        b_upper = bloque.upper()
        if "DENOMINACIÓN" in b_upper or "DENOMINACION" in b_upper:
            if ":" in bloque and len(bloque.split(":", 1)[1].strip()) > 3:
                info["nombre_programa"] = bloque.split(":", 1)[1].strip()
                break
            elif idx + 1 < len(bloques_p1):
                candidato = bloques_p1[idx + 1]
                if len(candidato) > 3 and "SENA" not in candidato.upper():
                    info["nombre_programa"] = candidato
                    break

    match_ver = re.search(r"Versi[oó]n[:\s]*(\d+)", texto_primeras, re.IGNORECASE)
    if match_ver:
        info["version"] = match_ver.group(1).strip()
    else:
        info["version"] = "1"

    matches_h = re.findall(r"\b(\d{3,4})\s*horas?\b", texto_primeras, re.IGNORECASE)
    if len(matches_h) >= 2:
        info["duracion_lectiva"] = f"{matches_h[0]} horas"
        prod_candidato = matches_h[1]
        if int(prod_candidato) > 1500 and len(matches_h) >= 3:
            prod_candidato = matches_h[2]
        info["duracion_productiva"] = f"{prod_candidato} horas"
        try:
            info["duracion_total"] = f"{int(matches_h[0]) + int(prod_candidato)} horas"
        except Exception:
            pass

    if len(doc) >= 2:
        texto_pag2 = str(doc[1].get_text("text"))
        candidatos_validos = [
            "Cajeros de Servicios Financieros",
            "Auxiliares de servicios financieros",
            "Auxiliares de Información y Servicio al Cliente",
        ]
        for cargo in candidatos_validos:
            if (
                cargo.lower() in texto_pag2.lower()
                and cargo not in info["perfiles_ocupacionales"]
            ):
                info["perfiles_ocupacionales"].append(cargo)

    doc.close()
    return info


def compilar_dom_competencias(ruta_pdf: str) -> Dict[str, Dict[str, Any]]:
    """Extrae las competencias oficiales del documento[cite: 13]."""
    competencias_dom = {}
    if not os.path.exists(ruta_pdf):
        return competencias_dom

    doc: fitz.Document = fitz.open(ruta_pdf)
    total_paginas = len(doc)
    lista_competencias = []

    for i in range(total_paginas):
        texto_pag = str(doc[i].get_text("text"))
        lineas = [l.strip() for l in texto_pag.splitlines() if l.strip()]

        for idx, linea in enumerate(lineas):
            l_upper = linea.upper()
            if "4.3" in l_upper or "NOMBRE DE LA COMPETENCIA" in l_upper:
                nombre_hallado = ""
                if ":" in linea:
                    partes = linea.split(":", 1)
                    candidato = partes[1].strip()
                    if len(candidato) > 8 and "4.3" not in candidato:
                        nombre_hallado = candidato

                if not nombre_hallado:
                    for offset in [1, 2, 3]:
                        if idx + offset < len(lineas):
                            sig = lineas[idx + offset]
                            if len(sig) > 12:
                                nombre_hallado = sig
                                break

                if nombre_hallado and len(nombre_hallado) > 10:
                    c_limpio = re.sub(r"^(?:[0-9\.\-\s]+)", "", nombre_hallado).strip(
                        " :.-"
                    )
                    if len(c_limpio) > 10 and c_limpio.upper() not in [
                        c["nombre"] for c in lista_competencias
                    ]:
                        lista_competencias.append(
                            {
                                "nombre": c_limpio.upper(),
                                "pagina_inicio": i + 1,
                                "pagina_fin": i + 1,
                                "texto_bloque": texto_pag,
                            }
                        )

    doc.close()
    for idx, comp in enumerate(lista_competencias, start=1):
        competencias_dom[f"{idx:02d}. {comp['nombre']}"] = comp

    return competencias_dom


def extraer_tablas_desde_dom(texto_bloque: str) -> Dict[str, List[str]]:
    """Extrae las tablas curriculares oficiales[cite: 13]."""
    tablas = {
        "resultados_aprendizaje": [],
        "conocimientos_proceso": [],
        "conocimientos_saber": [],
        "criterios_evaluacion": [],
    }
    seccion_activa = None
    for linea in texto_bloque.splitlines():
        l_trim = linea.strip()
        if not l_trim or len(l_trim) < 2:
            continue
        l_upper = l_trim.upper()

        if "4.5" in l_upper and "RESULTADO" in l_upper:
            seccion_activa = "RAP"
            continue
        elif "4.6.1" in l_upper or "PROCESO" in l_upper:
            seccion_activa = "PROCESO"
            continue
        elif "4.6.2" in l_upper or "SABER" in l_upper:
            seccion_activa = "SABER"
            continue
        elif "4.7" in l_upper or "CRITERIOS" in l_upper:
            seccion_activa = "CRITERIOS"
            continue

        if seccion_activa == "RAP":
            tablas["resultados_aprendizaje"].append(l_trim)
        elif seccion_activa == "PROCESO":
            tablas["conocimientos_proceso"].append(l_trim)
        elif seccion_activa == "SABER":
            tablas["conocimientos_saber"].append(l_trim)
        elif seccion_activa == "CRITERIOS":
            tablas["criterios_evaluacion"].append(l_trim)

    return tablas


def analizar_pagina_pdf(img_bgr: np.ndarray) -> Tuple[np.ndarray, dict]:
    """Aplica visión artificial a la página del PDF[cite: 13]."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gray_clahe = clahe.apply(gray)
    canny = cv2.Canny(gray_clahe, 50, 150)
    canny_rgb = cv2.cvtColor(canny, cv2.COLOR_GRAY2RGB)

    h, w = img_bgr.shape[:2]
    metricas = {
        "ancho": w,
        "alto": h,
        "resolucion_aprox": f"{w}x{h} px",
        "nivel_nitidez": float(cv2.Laplacian(gray, cv2.CV_64F).var()),
    }
    return canny_rgb, metricas
