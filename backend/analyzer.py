# backend/analyzer.py
import numpy as np
import logging
from sklearn.metrics.pairwise import cosine_similarity
from backend.db import fetch_keywords_for_component
from backend.nlp_pipeline import encode_sentences

# 🔹 CONFIG
WEIGHT_KEYWORD = 0.5
WEIGHT_SEMANTIC = 0.4
WEIGHT_ENTITY = 0.1

TOP_K = 3
MIN_RELEVANCE_THRESHOLD = 0.25

# 🔹 LOGGING
logger = logging.getLogger("analyzer")
logging.basicConfig(level=logging.INFO)


def classify_impact(score: float) -> str:
    if score > 0.75:
        return "HIGH"
    elif score > 0.45:
        return "MEDIUM"
    else:
        return "LOW"


def safe_cosine_similarity(a, b):
    try:
        if a.size and b.size:
            return cosine_similarity(a, b)
    except Exception as e:
        logger.error(f"Error computing similarity: {e}")
    return np.zeros((len(a), len(b)))


def score_components(components, fragments, emb, extracted):

    if not components:
        logger.warning("No components provided")
        return []

    if not fragments:
        logger.warning("No fragments extracted from document")

    # 🔹 MAP eficiente
    comp_map = {c['id']: c for c in components}

    # 🔹 Construcción de textos
    comp_ids = []
    comp_texts = []

    for c in components:
        comp_ids.append(c['id'])
        comp_texts.append(
            (c.get('nombre') or "") + ". " + (c.get('descripcion') or "")
        )

    # 🔹 Embeddings componentes
    try:
        comp_emb = encode_sentences(comp_texts)
    except Exception as e:
        logger.error(f"Embedding error: {e}")
        comp_emb = np.zeros((len(comp_texts), 384))

    # 🔹 Similaridad
    sim = safe_cosine_similarity(comp_emb, emb)

    results = []

    for i, cid in enumerate(comp_ids):

        comp = comp_map[cid]
        cname = comp.get("nombre", "Desconocido")
        ctype = comp.get("tipo", "N/A")

        try:
            kws = fetch_keywords_for_component(cid)
        except Exception as e:
            logger.error(f"DB error fetching keywords for {cid}: {e}")
            kws = []

        # =========================
        # 🔹 KEYWORD SCORE
        # =========================
        keyword_hits_per_fragment = []

        for frag in fragments:
            hits = sum(1 for k in kws if k.lower() in frag.lower())
            keyword_hits_per_fragment.append(hits)

        keyword_hits_per_fragment = np.array(keyword_hits_per_fragment)

        if len(kws) > 0:
            kw_score = min(1.0, keyword_hits_per_fragment.max() / len(kws))
        else:
            kw_score = 0.0

        # =========================
        # 🔹 SEMANTIC SCORE
        # =========================
        if sim.size:
            topk_vals = np.sort(sim[i])[-TOP_K:]
            sem_score = float(np.mean(topk_vals))
        else:
            sem_score = 0.0

        # =========================
        # 🔹 ENTITY SCORE
        # =========================
        ent_score = 0.0

        for txt, lab in extracted.get("entities", []):
            if txt.lower() in cname.lower():
                ent_score += 0.5
            if lab in ["LEY", "CONCEPTO_LEGAL"]:
                ent_score += 0.2

        ent_score = min(1.0, ent_score)

        # =========================
        # 🔹 FINAL SCORE
        # =========================
        final_score = (
            WEIGHT_KEYWORD * kw_score +
            WEIGHT_SEMANTIC * sem_score +
            WEIGHT_ENTITY * ent_score
        )

        impact = classify_impact(final_score)

        # =========================
        # 🔹 TOP FRAGMENTS
        # =========================
        top_fragments = []

        if sim.size:
            idxs = list(np.argsort(-sim[i])[:TOP_K])
        else:
            idxs = []

        for k in idxs:
            if k < len(fragments):
                score_val = float(sim[i, k])

                if score_val > MIN_RELEVANCE_THRESHOLD or keyword_hits_per_fragment[k] > 0:
                    top_fragments.append({
                        "fragment": fragments[k],
                        "semantic_score": score_val,
                        "keyword_hits": int(keyword_hits_per_fragment[k])
                    })

        # =========================
        # 🔹 EXPLANATION
        # =========================
        if final_score > 0.75:
            explanation = "Strong semantic similarity and keyword matches"
        elif final_score > 0.45:
            explanation = "Moderate relevance based on partial matches"
        else:
            explanation = "Low relevance or weak matches"

        # =========================
        # 🔹 RESULT
        # =========================
        results.append({
            "componente_id": cid,
            "component_name": cname,
            "tipo": ctype,
            "final_score": round(float(final_score), 4),
            "impact": impact,
            "scores": {
                "keyword": round(float(kw_score), 4),
                "semantic": round(float(sem_score), 4),
                "entity": round(float(ent_score), 4)
            },
            "top_fragments": top_fragments,
            "explanation": explanation,
            "debug": {
                "num_keywords": len(kws),
                "max_keyword_hits": int(keyword_hits_per_fragment.max()) if len(keyword_hits_per_fragment) else 0
            }
        })

    # 🔹 Orden final
    results = sorted(results, key=lambda r: -r["final_score"])

    logger.info(f"Scored {len(results)} components")

    return results