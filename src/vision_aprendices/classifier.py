import cv2
import numpy as np


def procesar_imagen_uniforme(img_pil, nombre_archivo="imagen.jpg"):
    """Procesa la fotografía del aprendiz SENA aplicando

    transformaciones de OpenCV y generando un diccionario
    con métricas institucionales y de georreferenciación.
    """
    img_array = np.array(img_pil)

    if len(img_array.shape) == 3 and img_array.shape[2] == 3:
        img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    else:
        img_bgr = img_array

    # 1. Transformación a escala de grises y detección de bordes
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)

    # 2. Métricas y cálculos para el reporte institucional
    alto, ancho = img_array.shape[:2]
    varianza_nitidez = float(np.var(gray.astype(float)))

    sena_centro = "Centro de Tecnología de la Manufactura"
    sena_sede = " Avanzada - SENA Antioquia"

    metricas = {
        "aprendiz": f"Aprendiz SENA ({nombre_archivo.split('.')[0]})",
        "centro_formacion": sena_centro + sena_sede,
        "programa_formacion": (
            "Gestión Contable y de Información Financiera / "
            "Sistematizar Datos Masivos"
        ),
        "ubicacion": ("Calle 51 # 57-70, Medellín, Antioquia, Colombia"),
        "lat": 6.2518,
        "lon": -75.5636,
        "nitidez": f"{varianza_nitidez:.1f} RMS",
        "resolucion": f"{ancho}x{alto} px",
        "blog_centro": "https://sena.edu.co",
        "foto_sede": (
            "https://images.unsplash.com/photo-1541339907198-"
            "e08756dedf3f?q=80&w=600&auto=format&fit=crop"
        ),
    }

    return edges_rgb, metricas
