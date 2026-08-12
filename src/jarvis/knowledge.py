import os
import glob
import re
import math
from typing import List, Dict


KNOWLEDGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "knowledge"))


class _KBIndex:
    def __init__(self):
        self.docs: List[Dict] = []
        self.doc_tokens: List[List[str]] = []
        self.df: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.built = False

    def _tokenize(self, text: str):
        tokens = [t.lower() for t in re.findall(r"\w+", text, flags=re.UNICODE)]
        # stopwords básicos en español e inglés
        stopwords = {
            "y","o","el","la","los","las","de","del","que","un","una","a","the","is","in","on","for","with","to","of","it"
        }
        filtered = [t for t in tokens if t not in stopwords]
        return filtered

    def load_docs(self):
        self.docs = []
        pattern = os.path.join(KNOWLEDGE_DIR, "**", "*.md")
        for path in glob.glob(pattern, recursive=True):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read()
                title = os.path.splitext(os.path.basename(path))[0]
                self.docs.append({"path": path, "title": title, "text": text})
            except Exception:
                continue

    def build(self):
        if not os.path.exists(KNOWLEDGE_DIR):
            self.built = True
            return
        self.load_docs()
        N = len(self.docs)
        self.doc_tokens = []
        self.df = {}
        for d in self.docs:
            tokens = self._tokenize(d.get("text", ""))
            self.doc_tokens.append(tokens)
            unique = set(tokens)
            for t in unique:
                self.df[t] = self.df.get(t, 0) + 1

        # compute idf
        self.idf = {}
        for term, df in self.df.items():
            self.idf[term] = math.log((N + 1) / (df + 1)) + 1.0
        self.built = True

    def score(self, query: str):
        if not self.built:
            self.build()
        if not self.docs:
            return []
        qtokens = [t for t in re.findall(r"\w+", query.lower())]
        scores = []
        for i, d in enumerate(self.docs):
            tokens = self.doc_tokens[i]
            if not tokens:
                scores.append((0.0, i))
                continue
            tf = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            # normalize tf
            L = len(tokens)
            for t in list(tf.keys()):
                tf[t] = tf[t] / L

            s = 0.0
            for qt in qtokens:
                s += tf.get(qt, 0.0) * self.idf.get(qt, 0.0)
            scores.append((s, i))
        scores.sort(key=lambda x: x[0], reverse=True)
        return scores


_INDEX = _KBIndex()


def search(query: str, top: int = 3) -> str:
    if not os.path.exists(KNOWLEDGE_DIR):
        return "No hay una base de conocimiento. Crea archivos Markdown en la carpeta 'knowledge'."

    scores = _INDEX.score(query)
    if not scores:
        return "No hay documentos en la base de conocimiento."

    out_lines = []
    found = 0
    for s, idx in scores:
        if s <= 0:
            continue
        d = _INDEX.docs[idx]
        # intentar extraer un fragmento relevante
        text = d.get("text", "")
        q = query.strip()
        m = None
        try:
            m = re.search(re.escape(q), text, flags=re.IGNORECASE)
        except Exception:
            m = None
        if not m:
            # buscar primer token
            toks = re.findall(r"\w+", q)
            for tok in toks:
                m = re.search(re.escape(tok), text, flags=re.IGNORECASE)
                if m:
                    break
        if m:
            start = max(0, m.start() - 120)
            excerpt = text[start : start + 240].strip()
        else:
            excerpt = text[:240].strip()

        out_lines.append(f"{d.get('title')}: {excerpt}...")
        found += 1
        if found >= top:
            break

    if not out_lines:
        return "No encontré información relevante en la base de conocimiento."

    return "\n\n".join(out_lines)


def summarize(query: str, max_sentences: int = 3) -> str:
    """Extractive summary: selecciona oraciones que contienen términos de la consulta."""
    if not os.path.exists(KNOWLEDGE_DIR):
        return "No hay una base de conocimiento."
    # construir índice si es necesario
    if not _INDEX.built:
        _INDEX.build()

    # buscar documentos ordenados
    scores = _INDEX.score(query)
    if not scores:
        return "No hay documentos en la base de conocimiento."

    qtokens = [t for t in re.findall(r"\w+", query.lower())]
    summaries = []
    added = 0
    for s, idx in scores:
        if s <= 0:
            continue
        d = _INDEX.docs[idx]
        text = d.get("text", "")
        # dividir en oraciones simples
        sents = re.split(r'(?<=[\.\!\?])\s+', text)
        # puntuar oraciones
        sent_scores = []
        for sent in sents:
            toks = [t.lower() for t in re.findall(r"\w+", sent)]
            score = sum(1 for qt in qtokens if qt in toks)
            if score > 0:
                sent_scores.append((score, sent.strip()))
        sent_scores.sort(key=lambda x: x[0], reverse=True)
        for score, sent in sent_scores[:max_sentences]:
            summaries.append(f"{d.get('title')}: {sent}")
            added += 1
            if added >= max_sentences:
                break
        if added >= max_sentences:
            break

    if not summaries:
        # fallback a fragments
        return search(query, top=1)

    return "\n".join(summaries)


def reload_index() -> int:
    """Reconstruye el índice y devuelve el número de documentos indexados."""
    _INDEX.build()
    return len(_INDEX.docs)
