import numpy as np
import requests
from bs4 import BeautifulSoup
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity


class ConectorBlogSena:
    """Conector dinamico avanzado para explotar

    todo el Blog del SENA.
    """

    def __init__(self, blog_url="https://sena-comercio.blogspot.com/"):
        self.blog_url = blog_url
        self.portal_nacional = "https://www.sena.edu.co"
        self.regional_antioquia = (
            "https://sena.edu.co/es-co/"
            "regionales/ZonaAndina/"
            "Paginas/antioquia.aspx"
        )

    def extraer_entradas(self):
        """Extrae de forma masiva entradas y

        contenido del blog institucional.
        """
        corpus_dinamico = []
        urls_posts_descubiertas = set()
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        # 1. Exploracion masiva de la pagina principal
        paginas_a_explorar = [self.blog_url]
        for i in range(1, 4):
            # Blogger usa parametro ?updated-max para paginar hacia atras
            paginas_a_explorar.append(f"{self.blog_url.rstrip('/')}?page={i}")

        for p_url in paginas_a_explorar:
            try:
                res = requests.get(p_url, headers=headers, timeout=6)
                if res.status_code == 200:
                    soup = BeautifulSoup(res.text, "html.parser")
                    for a in soup.find_all("a", href=True):
                        h_raw = a.get("href", "")
                        if not isinstance(h_raw, str):
                            continue
                        domain = "sena-comercio.blogspot.com"
                        if domain in h_raw and "google.com" not in h_raw:
                            patterns = ["/20", ".html", "/p/"]
                            if any(p in h_raw for p in patterns):
                                urls_posts_descubiertas.add(h_raw)
            except Exception:
                continue

        # 2. Extraccion profunda de cada post descubierto
        lista_urls = list(urls_posts_descubiertas)[:30]
        urls_procesadas = set()

        for u_post in lista_urls:
            if u_post in urls_procesadas:
                continue
            urls_procesadas.add(u_post)

            try:
                res_p = requests.get(u_post, headers=headers, timeout=5)
                if res_p.status_code == 200:
                    soup_p = BeautifulSoup(res_p.text, "html.parser")

                    for el in soup_p(
                        ["script", "style", "nav", "header", "footer", "aside"]
                    ):
                        el.decompose()

                    post_body = soup_p.find("div", class_="post-body")
                    if not post_body:
                        post_body = soup_p.find("div", class_="entry-content")
                    if not post_body:
                        post_body = soup_p.find("div", class_="main")
                    if not post_body:
                        post_body = soup_p

                    textos_bloques = [
                        elem.get_text(strip=True)
                        for elem in post_body.find_all(
                            ["p", "li", "td", "h1", "h2", "h3", "h4", "span"]
                        )
                        if len(elem.get_text(strip=True)) > 3
                    ]

                    txt_p = " ".join(textos_bloques)
                    if len(txt_p) < 50:
                        txt_p = post_body.get_text(separator=" ", strip=True)

                    if len(txt_p) > 20:
                        t_title = soup_p.find(["h1", "h2", "h3"])
                        titulo = (
                            t_title.get_text(strip=True)
                            if t_title
                            else "NOTICIAS Y EVENTOS SENA"
                        )

                        sub_txt = txt_p[:3500]
                        inf_txt = (
                            f"NOTICIA / HISTORIAL INSTITUCIONAL SENA - "
                            f"{titulo.upper()}. CONTENIDO: {sub_txt}"
                        )
                        corpus_dinamico.append(
                            {
                                "texto": inf_txt,
                                "url": u_post,
                            }
                        )
            except Exception:
                continue

        # 3. Inyeccion de portales regionales y plataformas clave
        corpus_dinamico.append(
            {
                "texto": (
                    "PORTAL OFICIAL DE LA REGIONAL ANTIOQUIA SENA. "
                    "INFORMACION INSTITUCIONAL, CONVOCATORIAS, NOTICIAS "
                    "DE LA ZONA ANDINA Y PROGRAMAS DE FORMACION "
                    "EN TODO EL DEPARTAMENTO DE ANTIOQUIA."
                ),
                "url": self.regional_antioquia,
            }
        )

        corpus_dinamico.append(
            {
                "texto": (
                    "BETOWA ES LA PLATAFORMA VIRTUAL Y DE SERVICIOS "
                    "TECNOLOGICOS DEL SENA EN ANTIOQUIA PARA LA GESTION "
                    "Y APOYO A LOS APRENDICES Y PROCESOS EDUCATIVOS."
                ),
                "url": "https://betowa.sena.edu.co/",
            }
        )

        corpus_dinamico.append(
            {
                "texto": (
                    "AGENCIA PUBLICA DE EMPLEO APE SENA. "
                    "PLATAFORMA NACIONAL Y REGIONAL PARA LA INTERMEDIACION "
                    "LABORAL, VACANTES DE EMPLEO, POSTULACIONES Y ORIENTACION "
                    "OCUPACIONAL PARA LOS COLOMBIANOS Y APRENDICES."
                ),
                "url": "https://ape.sena.edu.co/",
            }
        )

        corpus_dinamico.append(
            {
                "texto": (
                    "ZAJUNA ES LA PLATAFORMA VIRTUAL "
                    "OFICIAL DE APRENDIZAJE "
                    "DEL SERVICIO NACIONAL DE APRENDIZAJE "
                    "- SENA A NIVEL NACIONAL. "
                    "ESTA HERRAMIENTA TECNOLOGICA ESTA DISPONIBLE "
                    "PARA TODOS LOS APRENDICES DE COLOMBIA QUE DESEAN "
                    "FORMARSE DE FORMA VIRTUAL, DESARROLLAR CURSOS, "
                    "ACCEDER A CONTENIDOS ACADEMICOS Y GESTIONAR "
                    "SUS PROCESOS DE FORMACION EN LINEA."
                ),
                "url": "https://zajuna.sena.edu.co/",
            }
        )

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
                from sentence_transformers import SentenceTransformer

                self._model = SentenceTransformer(self.model_name)
            except ImportError:
                self.modelo_disponible = False

    def indexar_corpus(self, corpus_local=None, incluir_blog=True):
        """Indiza corpus local, limpiando URLs, e integra fuentes SENA."""
        corpus_data = []
        default_blog_url = "https://sena-comercio.blogspot.com/"

        if corpus_local:
            for item in corpus_local:
                url_limpia = item.get("url", default_blog_url)
                if "google.com/search" in url_limpia:
                    url_limpia = default_blog_url

                corpus_data.append(
                    {
                        "texto": item.get("texto", ""),
                        "url": url_limpia,
                    }
                )

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
