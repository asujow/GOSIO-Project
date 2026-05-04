# backend/app.py
import logging
import sys
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from backend.nlp_pipeline import pipeline_from_pdf
from backend.db import fetch_components
from backend.analyzer import score_components

app = FastAPI()

logger = logging.getLogger("backend")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    # leer archivo temporal
    contents = await file.read()
    # pipeline espera path o file-like; pdfplumber acepta BytesIO
    import io
    bio = io.BytesIO(contents)
    doc = pipeline_from_pdf(bio)
    components = fetch_components()
    
    results = score_components(components, doc["fragments"], doc["fragment_embeddings"], doc)
    return JSONResponse({"status":"ok","num_fragments":len(doc["fragments"]),"results":results})

@app.get("/components")
def components_list():
    comps = fetch_components()
    logger.info("components_list: %d componentes cargados", len(comps))
    return {"components": comps}