# flake8: noqa: E203, E501
import os
import re
import fitz  # PyMuPDF
from typing import List, Dict, Any


class ProfessionalSenaRAG:
    """Motor RAG empresarial con extracción dinámica de códigos NCL, nombres y duraciones para el SENA."""

    def __init__(self, directorio_raw: str = "data/raw") -> None:
        self.directorio_raw = directorio_raw
        self.documentos_indexados: List[Dict[str, Any]] = []
        self.codigo_activo: Any = None  # Memoria de sesión interna
        self._indexar_base_documental()

    def _indexar_base_documental(self) -> None:
        """Escanea la primera página y el contenido completo de cada PDF."""
        if not os.path.exists(self.directorio_raw):
            return

        archivos = os.listdir(self.directorio_raw)
        pdfs = [f for f in archivos if f.lower().endswith(".pdf")]

        for pdf_file in pdfs:
            ruta_pdf = os.path.join(self.directorio_raw, pdf_file)
            try:
                doc: Any = fitz.open(ruta_pdf)
                texto_portada = ""
                texto_completo = ""
                portada_lines = []

                if len(doc) > 0:
                    blocks = doc[0].get_text("blocks")
                    blocks_sorted = sorted(blocks, key=lambda b: (b[1], b[0]))
                    for b in blocks_sorted:
                        b_text = b[4].strip()
                        if b_text:
                            portada_lines.append(b_text)
                            texto_portada += b_text + "\n"

                for page in doc:
                    texto_completo += (page.get_text("text") or "") + "\n"

                codigo = "N/A"
                m_cod = re.search(
                    r"(?:1\.2\.\s*Código\s*Programa|código|codigo)(?:\s+del\s+programa)?[:\s]*(\d{5,6})",
                    texto_portada,
                    re.IGNORECASE,
                )
                if m_cod:
                    codigo = m_cod.group(1)
                else:
                    m_gen = re.search(r"\b(\d{5,6})\b", texto_portada)
                    if m_gen:
                        codigo = m_gen.group(1)

                self.documentos_indexados.append(
                    {
                        "archivo": pdf_file,
                        "codigo": codigo,
                        "portada_lines": portada_lines,
                        "texto_portada": texto_portada,
                        "contenido": texto_completo,
                    }
                )
                doc.close()
            except Exception:
                pass

    def consultar(self, query: str) -> str:
        """Recupera el documento por código y procesa dinámicamente la intención de la consulta."""
        query_clean = query.strip()
        query_lower = query_clean.lower()

        if any(
            s in query_lower
            for s in [
                "hola",
                "buenos dias",
                "buenas tardes",
                "buenas noches",
                "saludos",
            ]
        ):
            n_docs = len(self.documentos_indexados)
            return (
                f"¡Hola! 👋 Tengo indexados **{n_docs} diseños curriculares** oficiales.\n\n"
                f"Por favor, ingresa el **código del programa** (ej. `133303`) para consultar su información."
            )

        documento_seleccionado = None
        codigo_buscado = None

        numeros = re.findall(r"\b\d{5,6}\b", query)
        if numeros:
            codigo_buscado = numeros[0]
            self.codigo_activo = codigo_buscado
        elif self.codigo_activo:
            codigo_buscado = self.codigo_activo

        if codigo_buscado:
            for doc in self.documentos_indexados:
                if doc["codigo"] == codigo_buscado:
                    documento_seleccionado = doc
                    break

        if not documento_seleccionado:
            buscado = numeros[0] if numeros else query_clean
            return (
                f"❌ No encontré ningún diseño curricular asociado al código **{buscado}**.\n\n"
                f"💡 *Sugerencia:* Ingresa primero el código del programa (ej. `133303`) para establecer la consulta."
            )

        # Si el usuario pregunta explícitamente por competencias
        if "competencia" in query_lower or "competencias" in query_lower:
            return self._extraer_competencias_43(documento_seleccionado, query_clean)

        return self._extraer_y_formatear(documento_seleccionado, query_clean)

    def _extraer_denominacion_portada(self, portada_lines: List[str]) -> str:
        """Extrae la denominación del programa desde las líneas de la portada."""
        denominacion = "No especificado"
        for i, line in enumerate(portada_lines):
            if (
                "denominación" in line.lower()
                or "denominacion" in line.lower()
                or "1.1" in line
            ):
                for separator in [":", "-"]:
                    if separator in line:
                        parts = line.split(separator, 1)
                        candidate = parts[1].strip()
                        candidate_clean = re.sub(
                            r"^(?:del\s+programa[\s:\-]*)+",
                            "",
                            candidate,
                            flags=re.IGNORECASE,
                        ).strip()
                        if len(candidate_clean) > 3 and not any(
                            w in candidate_clean.lower()
                            for w in [
                                "vigente",
                                "estado",
                                "denominación",
                                "del programa",
                            ]
                        ):
                            denominacion = candidate_clean
                            break
                if denominacion != "No especificado":
                    break
                for offset in range(1, 4):
                    if i + offset < len(portada_lines):
                        next_line = portada_lines[i + offset].strip()
                        cleaned = re.sub(
                            r"^(?:\d+[\.\)]\s*)?(?:denominación|denominacion)?\s*(?:del\s+programa)?[:\-\s]*",
                            "",
                            next_line,
                            flags=re.IGNORECASE,
                        ).strip()
                        cleaned = re.sub(
                            r"^(?:del\s+programa[:\-\s]*)",
                            "",
                            cleaned,
                            flags=re.IGNORECASE,
                        ).strip()
                        if (
                            len(cleaned) > 3
                            and cleaned.lower()
                            not in [
                                "del programa",
                                "del programa:",
                                "denominacion del programa",
                            ]
                            and not any(
                                w in cleaned.lower() for w in ["vigente", "estado"]
                            )
                        ):
                            denominacion = cleaned
                            break
                if denominacion != "No especificado":
                    break
        return denominacion

    def _extraer_competencias_43(self, documento: Dict[str, Any], query: str) -> str:
        """Extrae de manera dinámica los códigos NCL, los nombres reales y las duraciones de las 14 competencias."""
        contenido = documento["contenido"]
        codigo = documento["codigo"]
        portada_lines = documento["portada_lines"]

        denominacion = self._extraer_denominacion_portada(portada_lines)
        competencias_lista = []

        # Encontrar todas las ocurrencias de códigos de norma de competencia laboral (NCL de 9 dígitos)
        matches_ncl = list(re.finditer(r"\b(\d{9})\b", contenido))

        for m in matches_ncl:
            ncl_code = m.group(1)
            pos = m.end()
            fragmento = contenido[pos : pos + 800]

            # Dividir por líneas para limpiar y encontrar el texto real de la competencia
            lineas = [l.strip() for l in fragmento.split("\n") if l.strip()]
            nombre_comp = ""

            for linea in lineas:
                # Omitir líneas cortas, números de página o metadatos
                if len(linea) > 10 and not re.match(
                    r"^(\d+|4\.\d+|p[áa]gina)", linea, re.IGNORECASE
                ):
                    if not any(
                        w in linea.lower()
                        for w in [
                            "versión",
                            "version",
                            "resultados",
                            "aprendizaje",
                            "norma",
                            "sena",
                        ]
                    ):
                        nombre_comp = linea.upper()
                        break

            if not nombre_comp:
                nombre_comp = "COMPETENCIA DEL PROGRAMA"

            # Extraer la duración estimada (Item 4.4)
            duracion = "48 horas"
            m_dur = re.search(r"(\d{2,4}\s*horas?)", fragmento, re.IGNORECASE)
            if m_dur:
                m_num = re.search(r"(\d{2,4})", m_dur.group(1))
                if m_num:
                    duracion = f"{m_num.group(1)} horas"

            item_formateado = (
                f"[`{ncl_code}`] **{nombre_comp}** *(Duración: {duracion})*"
            )
            if (
                item_formateado not in competencias_lista
                and len(competencias_lista) < 14
            ):
                competencias_lista.append(item_formateado)

        encabezado = f"* **Nombre del Programa:** **{denominacion}**\n\n"

        if not competencias_lista:
            return (
                f"### 📚 Competencias, Códigos y Duración (`{codigo}`)\n\n"
                f"{encabezado}"
                f"⚠️ No se lograron aislar las competencias en este documento."
            )

        lista_formateada = "\n".join(
            [f"{idx + 1}. {c}" for idx, c in enumerate(competencias_lista)]
        )

        return (
            f"### 📚 Competencias, Códigos y Duración (`{codigo}`)\n\n"
            f"{encabezado}"
            f"**Competencias registradas en el diseño curricular ({len(competencias_lista)} en total):**\n\n"
            f"{lista_formateada}\n"
        )

    def _extraer_y_formatear(self, documento: Dict[str, Any], query: str) -> str:
        """Extrae con precisión milimétrica los campos institucionales de la portada."""
        portada_lines = documento["portada_lines"]
        texto_portada = documento["texto_portada"]
        codigo = documento["codigo"]
        q_lower = query.lower()

        denominacion = self._extraer_denominacion_portada(portada_lines)

        version = "1"
        m_ver = re.search(
            r"1\.3\.?\s*(?:Versión|version)[^\d]*(\d{1,2})",
            texto_portada,
            re.IGNORECASE,
        )
        if m_ver:
            version = m_ver.group(1).strip()

        fecha_inicio = "No especificado"
        m_vig = re.search(r"([\d]{1,2}[\/\-][\d]{1,2}[\/\-][\d]{4})", texto_portada)
        if m_vig:
            fecha_inicio = m_vig.group(1).strip()

        lectiva = "No especificado"
        productiva = "No especificado"

        todos_numeros = re.findall(r"\b(\d{3,4})\b", texto_portada)
        horas_candidatas = []
        for n_str in todos_numeros:
            val = int(n_str)
            if 300 <= val <= 4000 and not (2000 <= val <= 2030) and n_str != codigo:
                if n_str not in horas_candidatas:
                    horas_candidatas.append(n_str)

        if len(horas_candidatas) >= 1:
            lectiva = f"{horas_candidatas[0]} horas"
        if len(horas_candidatas) >= 2:
            productiva = f"{horas_candidatas[1]} horas"

        tipo_programa = (
            "TITULADO"
            if "titulado" in texto_portada.lower()
            else (
                "Tecnólogo"
                if "tecnólogo" in texto_portada.lower()
                or "tecnologo" in texto_portada.lower()
                else "Técnico"
            )
        )

        titulo_certificado = "No especificado"
        for i, line in enumerate(portada_lines):
            line_upper = line.upper()
            if "1.7" in line or "TÍTULO" in line_upper or "TITULO" in line_upper:
                for offset in range(0, 4):
                    if i + offset < len(portada_lines):
                        cand = portada_lines[i + offset].strip().upper()
                        if "TECNÓLOGO" in cand or "TECNOLOGO" in cand:
                            titulo_certificado = "TECNÓLOGO"
                            break
                        elif "TÉCNICO" in cand or "TECNICO" in cand:
                            titulo_certificado = "TÉCNICO"
                            break
                if titulo_certificado != "No especificado":
                    break

        if titulo_certificado == "No especificado":
            titulo_certificado = (
                "TECNÓLOGO"
                if "tecnólogo" in texto_portada.lower()
                or "tecnologo" in texto_portada.lower()
                else f"Título en {denominacion}"
            )

        is_specific = any(
            kw in q_lower
            for kw in [
                "hora",
                "lectiva",
                "productiva",
                "tipo",
                "título",
                "titulo",
                "certificado",
                "vigencia",
                "fecha",
                "inicio",
                "versión",
                "version",
                "programa",
                "pertenece",
                "nombre",
            ]
        )

        detalles = []

        if not is_specific:
            detalles = [
                f"* **Nombre del Programa:** **{denominacion}**",
                f"* **Código Institucional:** `{codigo}`",
            ]
        else:
            if any(
                k in q_lower
                for k in [
                    "programa",
                    "nombre",
                    "pertenece",
                    "denominación",
                    "denominacion",
                ]
            ):
                detalles.append(f"* **Nombre del Programa:** **{denominacion}**")
            if any(k in q_lower for k in ["versión", "version"]):
                detalles.append(f"* **Versión del Programa:** {version}")
            if any(k in q_lower for k in ["vigencia", "fecha", "inicio"]):
                detalles.append(f"* **Fecha de Inicio / Vigencia:** {fecha_inicio}")
            if any(k in q_lower for k in ["lectiva", "horas lectivas"]):
                detalles.append(f"* **Duración Etapa Lectiva:** {lectiva}")
            if any(k in q_lower for k in ["productiva", "horas productivas"]):
                detalles.append(f"* **Duración Etapa Productiva:** {productiva}")
            if any(k in q_lower for k in ["tipo"]):
                detalles.append(f"* **Tipo de Programa:** {tipo_programa}")
            if any(k in q_lower for k in ["título", "titulo", "certificado"]):
                detalles.append(f"* **Título o Certificado:** {titulo_certificado}")

            if not detalles:
                detalles = [
                    f"* **Nombre del Programa:** **{denominacion}**",
                    f"* **Código Institucional:** `{codigo}`",
                ]

        contenido_formateado = "\n".join(detalles)

        return (
            f"### 📋 Información del Diseño Curricular (`{codigo}`)\n\n"
            f"{contenido_formateado}\n"
        )
