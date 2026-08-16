import asyncio
import fitz
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .extractor import extract_entities, extract_obligations
from .graph_engine import FRDGEngine
from .graph_retrieval import GraphRAGRetriever
from .llm import extract_with_llm
from .models import AnalyzeTextRequest
from .recommendations import generate_recommendations

app = FastAPI(
    title="Graph-Based Operational Compliance Intelligence API",
    version="0.1.0",
    description="Prototype API for Financial Regulatory Dependency Graph impact analysis.",
)

origins = [x.strip() for x in settings.cors_origins.split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = FRDGEngine()
retriever = GraphRAGRetriever(engine)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "FRDG",
        "nodes": engine.graph.number_of_nodes(),
        "edges": engine.graph.number_of_edges(),
    }

@app.get("/api/graph")
def get_graph():
    return engine.graph_json()

async def analyze_text(text: str, source_label: str = "Uploaded Regulation"):
    obligations = extract_obligations(text)
    entities = extract_entities(text)
    llm_result = None

    if settings.llm_enabled and settings.openai_api_key:
        try:
            llm_result = await extract_with_llm(text)
        except Exception:
            llm_result = None

    topics = list(entities.keys())
    if llm_result:
        topics.extend(
            t.lower().replace(" ", "_")
            for t in llm_result.get("topics", [])
            if isinstance(t, str)
        )
        if llm_result.get("obligations"):
            obligations = llm_result["obligations"][:12]

    source_id = engine.infer_source(topics)
    impacted, counts, paths, risk = engine.impact(source_id)
    graph_evidence = retriever.retrieve(source_id)
    source_attrs = engine.graph.nodes[source_id]

    return {
        "source_id": source_id,
        "source_label": source_attrs.get("label", source_label),
        "source_type": source_attrs.get("type", "Regulation"),
        "risk_score": risk,
        "summary": (
            f"{source_attrs.get('label', source_label)} propagates through "
            f"{len(impacted)} downstream enterprise dependencies. "
            f"The highest-risk path reaches "
            f"{max([x['risk'] for x in impacted], default=risk):.0f}/100."
        ),
        "impacted": impacted,
        "counts": counts,
        "recommendations": generate_recommendations(impacted),
        "evidence_paths": paths,
        "graph_evidence": graph_evidence,
        "extracted_obligations": obligations,
    }

@app.post("/api/analyze-text")
async def analyze_text_endpoint(request: AnalyzeTextRequest):
    if len(request.text.strip()) < 20:
        raise HTTPException(status_code=400, detail="Please provide more regulatory text.")
    return await analyze_text(request.text, request.source_label or "Uploaded Regulation")

@app.post("/api/analyze-pdf")
async def analyze_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    content = await file.read()
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="PDF is larger than 15 MB.")

    try:
        document = fitz.open(stream=content, filetype="pdf")
        text = "\n".join(page.get_text() for page in document)
        document.close()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Could not read PDF: {exc}")

    if len(text.strip()) < 20:
        raise HTTPException(
            status_code=400,
            detail="The PDF contains too little extractable text. OCR is required for scanned PDFs.",
        )

    return await analyze_text(text, file.filename)
