# Graph-Based Operational Compliance Intelligence for Financial Institutions

A working prototype for the Singapore India Hackathon 2026 idea:

**Graph-Based Operational Compliance Intelligence for Financial Institutions**

The prototype turns a regulatory document into an explainable **Financial Regulatory Dependency Graph (FRDG)** and propagates regulatory impact across policies, business processes, APIs, microservices, databases, compliance controls, business units and audit artifacts.

## Implemented

- Regulatory PDF upload with FastAPI
- PDF text extraction with PyMuPDF
- Rule-based obligation/entity extraction
- Optional OpenAI-compatible LLM extraction (OpenAI, Llama 3 via compatible endpoint, etc.)
- Financial Regulatory Dependency Graph with NetworkX
- Explainable multi-hop impact propagation
- Risk scoring and dependency traces
- SyntheticBank-360 demo graph
- React + Cytoscape.js interactive graph
- Impact summary and recommended actions
- Graph-grounded retrieval layer (GraphRAG-style)
- Optional Neo4j and PyTorch Geometric integrations

The default demo runs without an API key, Neo4j instance, or trained GNN, so it is easy to demonstrate on a normal laptop.

## Architecture

```text
Regulatory PDF
      |
      v
  PDF Parser
      |
      v
Clause / Obligation Extraction
      |
      +-------------------+
      |                   |
      v                   v
  Optional LLM       Rule-based fallback
      |                   |
      +---------+---------+
                |
                v
 Financial Regulatory Dependency Graph
                |
        +-------+-------+-------+
        |               |       |
        v               v       v
     GraphRAG       Impact     GNN*
     retrieval    propagation
        |               |
        +-------+-------+
                |
                v
 Explainable recommendations
                |
                v
 React + Cytoscape dashboard

* Optional PyTorch Geometric scaffold.
```

## Repository structure

```text
Graph-Based-Impact-Analysis/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── extractor.py
│   │   ├── graph_engine.py
│   │   ├── gnn.py
│   │   ├── llm.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── recommendations.py
│   ├── tests/
│   │   ├── __init__.py
│   │   └── test_graph.py
│   ├── requirements.txt
│   ├── requirements-optional.txt
│   └── .env.example
├── data/
│   ├── synthetic_bank_360.json
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GraphView.jsx
│   │   │   ├── ImpactPanel.jsx
│   │   │   └── UploadPanel.jsx
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── styles.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── docker-compose.yml
├── GITHUB_SETUP.md
├── CONTRIBUTING.md
├── .gitignore
└── LICENSE
```

## Run locally

### Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Open the Vite URL, normally `http://localhost:5173`.

### Optional LLM

Copy `backend/.env.example` to `backend/.env` and set:

```env
LLM_ENABLED=true
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
```

The extractor falls back automatically if the LLM is unavailable.

### Optional Neo4j / GNN

```bash
docker compose --profile neo4j up neo4j
```

For optional ML/graph packages:

```bash
pip install -r backend/requirements-optional.txt
```

## Demo flow

1. Start the backend and frontend.
2. The dashboard loads the SyntheticBank-360 graph.
3. Click a regulation node.
4. Downstream dependencies are highlighted.
5. The impact panel shows affected policies, APIs, processes, controls, business units and audit artifacts.
6. Upload a regulatory PDF.
7. The backend extracts obligations, maps them to graph topics and returns an impact analysis.
8. The dependency trace explains paths such as:

```text
Regulatory Clause
 → Internal Policy
 → Business Process
 → API / Microservice
 → Database
 → Compliance Control
 → Audit Artifact
```

## Important scope note

This is a **decision-support prototype**, not an autonomous regulatory compliance system. Production deployment requires institution-specific inventories, validated regulatory ontologies, access controls, model evaluation, audit logging, human approval and legal/compliance review.

## Research contribution

The core idea is the **Financial Regulatory Dependency Graph (FRDG)**: a heterogeneous operational graph connecting regulatory obligations to the enterprise assets that implement them. The key value is multi-hop dependency reasoning rather than merely summarizing regulations.

## License

MIT.
