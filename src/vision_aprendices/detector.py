import os
import re
import cv2
import numpy as np
from PIL import Image
import streamlit as st
from ultralytics import YOLO

try:
    import easyocr

    reader = easyocr.Reader(["es"], gpu=False)
except Exception:
    reader = None


class SenaVisionProcessor:
    """Procesador dinámico de visión artificial."""

    def __init__(self, model_path="data/model/yolov8n.pt"):
        self.model_path = model_path
        self.model = None
        self.oferta_db = self._cargar_base_oferta()
        self._cargar_modelo()

    def _obtener_ruta_base(self):
        """Calcula la ruta base absoluta."""
        curr = os.path.dirname(os.path.abspath(__file__))
        return os.path.abspath(os.path.join(curr, "../../"))

    def _cargar_base_oferta(self):
        """Parsea la oferta institucional."""
        oferta_map = {}
        base_dir = self._obtener_ruta_base()
        path_oferta = os.path.join(base_dir, "data", "oferta_medellin.txt")

        if os.path.exists(path_oferta):
            try:
                with open(path_oferta, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue

                        match = re.search(r"\(([^)]+)\)", line)
                        if match:
                            sigla = match.group(1).strip().upper()
                            nombre_centro = line.split("(")[0].strip()
                        else:
                            parts = line.split(",")
                            nombre_centro = parts[0].strip()
                            sw = ["de", "la", "el", "los", "las", "en", "y"]
                            words = []
                            for p in nombre_centro.split():
                                if p.lower() not in sw:
                                    words.append(p)
                            sigla = "".join([w[0].upper() for w in words if w])

                        parts = line.split(",")
                        muni = "Medellín"
                        dept = "Antioquia"

                        if len(parts) > 1:
                            ub = parts[1].strip().split()
                            if len(ub) > 0:
                                muni = ub[0].strip()
                            if len(ub) > 1:
                                dept = ub[1].strip()

                        oferta_map[sigla] = {
                            "centro": nombre_centro,
                            "municipio": muni,
                            "departamento": dept,
                        }
            except Exception as e:
                print(f"Error: {e}")
        return oferta_map

    def _cargar_modelo(self):
        """Carga YOLO con seguridad."""
        try:
            base_dir = self._obtener_ruta_base()
            full_path = os.path.join(base_dir, self.model_path)
            if os.path.exists(full_path):
                self.model = YOLO(full_path)
            else:
                self.model = YOLO("yolov8n.pt")
        except Exception as e:
            print(f"Error YOLO: {e}")

    def extraer_programa_ocr(self, img_path):
        """Extrae el programa vía OCR."""
        default_prog = "Técnico en Servicios Comerciales"
        if not os.path.exists(img_path):
            return default_prog

        try:
            img = cv2.imread(img_path)
            if img is not None:
                h, w, _ = img.shape
                y1 = int(h * 0.50)
                y2 = int(h * 0.98)
                x1 = int(w * 0.50)
                roi = img[y1:y2, x1:w]

                if reader is not None:
                    res = reader.readtext(roi, detail=0)
                    str_list = []
                    for r in res:
                        txt = str(r).strip()
                        cond_l = len(txt) > 2
                        cond_s = "SENA" not in txt.upper()
                        if cond_l and cond_s:
                            str_list.append(txt)
                    if str_list:
                        detected = " ".join(str_list).strip()
                        if len(detected) > 5:
                            return detected
        except Exception:
            pass

        return default_prog

    def _limpiar_nombre_aprendiz(self, archivo):
        """Limpia el nombre del archivo."""
        base = (
            archivo.upper()
            .replace(".JPG", "")
            .replace(".PNG", "")
            .replace(".JPEG", "")
            .replace("APRENDIZ", "")
        )
        norm = base.replace("_", " ")

        keys = list(self.oferta_db.keys())
        sorted_keys = sorted(keys, key=len, reverse=True)
        for sigla in sorted_keys:
            s_norm = sigla.replace("_", " ")
            norm = norm.replace(s_norm, "").replace(sigla, "")

        return norm.strip().title()

    def obtener_lista_aprendices(self):
        """Obtiene el diccionario de aprendices."""
        base_dir = self._obtener_ruta_base()
        raw_dir = os.path.join(base_dir, "data", "raw", "aprendices")

        aprendices_dict = {}
        if os.path.exists(raw_dir):
            archivos = os.listdir(raw_dir)
            for archivo in archivos:
                if archivo.lower().endswith((".png", ".jpg", ".jpeg")):
                    limpio = self._limpiar_nombre_aprendiz(archivo)
                    full_path = os.path.join(raw_dir, archivo)
                    up_arq = archivo.upper().replace("_", " ")

                    info = {}
                    for sigla, datos in self.oferta_db.items():
                        s_norm = sigla.replace("_", " ")
                        if s_norm in up_arq or sigla in archivo.upper():
                            info = datos
                            break

                    centro = info.get("centro", "Centro de Formación SENA")
                    muni = info.get("municipio", "Medellín")
                    dept = info.get("departamento", "Antioquia")

                    prog = self.extraer_programa_ocr(full_path)

                    p_nombre = limpio.split()[0].upper() if limpio else ""
                    fem_suffix = ("A", "Y", "IS", "TH")
                    if p_nombre.endswith(fem_suffix):
                        genero = "Femenino"
                    else:
                        genero = "Masculino"

                    aprendices_dict[limpio] = {
                        "ruta": full_path,
                        "centro": centro,
                        "programa": prog,
                        "municipio": muni,
                        "departamento": dept,
                        "genero": genero,
                    }
        return aprendices_dict

    def procesar_imagen(self, image_path):
        """Procesa imagen con YOLO."""
        if not os.path.exists(image_path):
            return None, []

        try:
            img_pil = Image.open(image_path).convert("RGB")
            img_np = np.array(img_pil)

            res = []
            if self.model:
                res = list(self.model(img_np))
                if res and len(res) > 0:
                    annotated = res[0].plot()  # type: ignore
                    return Image.fromarray(annotated), res

            return img_pil, res
        except Exception as e:
            st.error(f"Error: {e}")
            return None, []
