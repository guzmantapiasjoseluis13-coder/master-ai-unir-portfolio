import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity


class ConectorBlogSena:
    """Conector 100% dinamico con etiquetado semantico por pestana."""

    def __init__(self, blog_url="https://sena-comercio.blogspot.com/"):
        self.blog_url = blog_url

    def extraer_entradas(self):
        """Descubre y mapea dinamicamente las secciones del menu."""
        corpus_dinamico = []
        mapa_urls_claves = {}
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; "
                "Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        keywords = [
            "directorio",
            "servicios",
            "nosotros",
            "aprendices",
            "programas",
            "portales",
            "egresados",
            "galeria",
        ]

        try:
            res = requests.get(self.blog_url, headers=headers, timeout=8)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                for a in soup.find_all("a", href=True):
                    t_link = a.get_text(strip=True).lower()
                    h_raw = a.get("href", "")
                    if isinstance(h_raw, list):
                        h_str = " ".join(h_raw)
                    else:
                        h_str = str(h_raw or "")

                    if h_str.startswith("/"):
                        h_str = self.blog_url.rstrip("/") + h_str
                    elif not h_str.startswith("http"):
                        continue

                    if "sena-comercio.blogspot.com" in h_str:
                        for k in keywords:
                            matched = k in t_link or k in h_str.lower()
                            if matched and k not in mapa_urls_claves:
                                mapa_urls_claves[k] = h_str
        except Exception:
            pass

        # Si la raiz no esta mapeada, incluirla como respaldo general
        if not mapa_urls_claves:
            mapa_urls_claves["institucional"] = self.blog_url

        # Extraer y etiquetar el contenido especifico
        # de cada pestana descubierta
        for clave, u_menu in mapa_urls_claves.items():
            try:
                res_p = requests.get(u_menu, headers=headers, timeout=5)
                if res_p.status_code == 200:
                    soup_p = BeautifulSoup(res_p.text, "html.parser")
                    post_body = soup_p.find("div", class_="post-body")
                    if not post_body:
                        post_body = soup_p.find("div", class_="entry-content")
                    if not post_body:
                        post_body = soup_p

                    txt_p = post_body.get_text(strip=True)
                    if len(txt_p) > 20:
                        t_title = soup_p.find(["h1", "h2", "h3"])
                        if t_title:
                            titulo = t_title.get_text(strip=True)
                        else:
                            titulo = clave.capitalize()

                        sub_txt = txt_p[:1200]
                        inf_txt = (
                            f"INFORMACION DE {clave.upper()} - "
                            f"{titulo.upper()}. {sub_txt}"
                        )
                        corpus_dinamico.append(
                            {
                                "texto": inf_txt,
                                "url": u_menu,
                            }
                        )
            except Exception:
                continue

        if not corpus_dinamico:
            corpus_dinamico.append(
                {
                    "texto": (
                        "CENTRO DE COMERCIO Y SERVICIOS MEDELLIN "
                        "REGIONAL ANTIOQUIA SITIO OFICIAL."
                    ),
                    "url": self.blog_url,
                }
            )

        return corpus_dinamico


class BuscadorVectorial:
    """Motor de busqueda semantica vectorial con PCA 2D."""

    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._model = None
        self.modelo_disponible = True
        self.corpus_texts = []
        self.corpus_urls = []
        self.corpus_embeddings = None
        self.pca_model = None
        self.corpus_2d = None

    def _load_model(self):
        """Carga perezosa de SentenceTransformer."""
        if self._model is None and self.modelo_disponible:
            try:
                from sentence_transformers import (
                    SentenceTransformer,
                )

                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                self.modelo_disponible = False

    def indexar_corpus(self, corpus_local=None, incluir_blog=True):
        """Indiza corpus local e integra el blog."""
        corpus_data = []

        if corpus_local:
            corpus_data.extend(corpus_local)

        if incluir_blog:
            conector = ConectorBlogSena()
            entradas_blog = conector.extraer_entradas()
            if entradas_blog:
                corpus_data.extend(entradas_blog)

        if not corpus_data:
            return

        self.corpus_texts = [item["texto"] for item in corpus_data]
        self.corpus_urls = [item["url"] for item in corpus_data]

        self._load_model()

        if self._model is not None:
            self.corpus_embeddings = self._model.encode(
                self.corpus_texts, convert_to_numpy=True
            )
        else:
            fallback = self._fallback_embeddings(self.corpus_texts)
            self.corpus_embeddings = fallback

        n_components = min(2, len(self.corpus_texts))
        if n_components >= 2:
            self.pca_model = PCA(n_components=2)
            transformed = self.pca_model.fit_transform(self.corpus_embeddings)
            self.corpus_2d = transformed
        else:
            self.corpus_2d = np.zeros((len(self.corpus_texts), 2))

    def _fallback_embeddings(self, texts):
        """Genera matriz sintetica."""
        np.random.seed(42)
        return np.random.rand(len(texts), 384)

    def buscar(self, query, top_k=3):
        """Busqueda vectorial por coseno."""
        if not self.corpus_texts or self.corpus_embeddings is None:
            return [], None, 0.0

        self._load_model()

        if self._model is not None:
            encoded_query = self._model.encode([query], convert_to_numpy=True)
            query_embedding = encoded_query
        else:
            seed_val = abs(hash(query)) % (2**32)
            np.random.seed(seed_val)
            query_embedding = np.random.rand(1, 384)

        sim_matrix = cosine_similarity(query_embedding, self.corpus_embeddings)
        similarities = sim_matrix[0]

        top_indices = np.argsort(similarities)[::-1][:top_k]

        resultados = []
        for idx in top_indices:
            resultados.append(
                {
                    "texto": self.corpus_texts[idx],
                    "url": self.corpus_urls[idx],
                    "score": float(similarities[idx]),
                    "index": int(idx),
                }
            )

        if self.pca_model is not None:
            query_2d = self.pca_model.transform(query_embedding)[0]
        else:
            query_2d = np.array([0.0, 0.0])

        score_promedio = float(np.mean(similarities[top_indices]))

        return (
            resultados,
            query_2d,
            score_promedio,
        )
