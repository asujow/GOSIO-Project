# backend/nlp_pipeline.py
import re
import pdfplumber
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from spacy.lang.en import English

def extract_text_from_pdf(path_or_bytes):
    text = []
    try:
        with pdfplumber.open(path_or_bytes) as pdf:
            for p in pdf.pages:
                t = p.extract_text()
                if t:
                    text.append(t)
        return "\n".join(text)

    except Exception as e:
        # 🔥 Fallback: tratar como texto plano
        try:
            if hasattr(path_or_bytes, "read"):
                path_or_bytes.seek(0)
                raw = path_or_bytes.read()
                return raw.decode("utf-8", errors="ignore")
        except Exception:
            pass

        print("Error leyendo PDF:", e)
        return ""

# Try to load en_core_web_lg, fallback to en_core_web_sm
try:
    nlp = spacy.load("en_core_web_lg")
except OSError:
    nlp = spacy.load("en_core_web_sm")

# Add custom entity ruler for legal concepts
ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "LEY", "pattern": [{"LOWER": "law"}, {"IS_DIGIT": True}]},
    {"label": "LEY", "pattern": [{"LOWER": "article"}, {"IS_DIGIT": True}]},
    {"label": "LEY", "pattern": [{"LOWER": "section"}, {"IS_DIGIT": True}]},
    {"label": "CONCEPTO_LEGAL", "pattern": [{"LOWER": "due"}, {"LOWER": "process"}]},
    {"label": "CONCEPTO_LEGAL", "pattern": [{"LOWER": "habeas"}, {"LOWER": "corpus"}]},
    {"label": "CONCEPTO_LEGAL", "pattern": [{"LOWER": "constitutional"}, {"LOWER": "right"}]},
    # Add more patterns as needed
]
ruler.add_patterns(patterns)  # type: ignore

model = SentenceTransformer("all-MiniLM-L6-v2")

def clean_and_normalize_text(text):
    # Remove extra whitespace and normalize line breaks
    text = re.sub(r'\r\n?', '\n', text)
    text = re.sub(r'\n{2,}', '\n\n', text)
    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)
    # Strip leading/trailing whitespace
    text = text.strip()
    return text

def extract_entities_and_chunks(text):
    doc = nlp(text)
    entities = [(e.text, e.label_) for e in doc.ents]
    noun_chunks = list(set([c.text.strip() for c in doc.noun_chunks if len(c.text.strip().split()) > 1]))  # Filter single words
    sentences = [s.text.strip() for s in doc.sents if s.text.strip()]
    return {"entities": entities, "noun_chunks": noun_chunks, "sentences": sentences}

def extract_key_terms_tfidf(text, top_n=10):
    # Use TF-IDF to extract key terms
    vectorizer = TfidfVectorizer(max_features=100)
    tfidf_matrix = vectorizer.fit_transform([text])
    feature_names = vectorizer.get_feature_names_out()
    scores = tfidf_matrix.toarray()[0]  # type: ignore
    top_terms = [feature_names[i] for i in scores.argsort()[-top_n:][::-1]]
    return top_terms

def encode_sentences(sents):
    embs = model.encode(sents, convert_to_numpy=True)
    return normalize(embs)

def pipeline_from_pdf(path_or_bytes):
    raw = extract_text_from_pdf(path_or_bytes)
    text = clean_and_normalize_text(raw)
    extracted = extract_entities_and_chunks(text)
    key_terms = extract_key_terms_tfidf(text)
    fragments = [p.strip() for p in re.split(r'\n{1,2}', text) if p.strip()]
    emb = encode_sentences(fragments)
    return {"text": text, "fragments": fragments, "fragment_embeddings": emb, "key_terms": key_terms, **extracted}
