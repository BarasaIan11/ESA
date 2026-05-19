# ESA — ERP Support Assistant

ESA is an AI-powered support assistant specialized in Microsoft Dynamics 365 Business Central. It provides a conversational interface for users to ask questions, troubleshoot issues, and get guidance on using Business Central effectively.

> **Knowledge base and vector store are hosted externally** (Pinecone + cloud storage) and are not part of this repository. See [Knowledge Base Setup](#-knowledge-base-setup) below.

---

## 🏗 Architecture

The project is structured as a monorepo containing a modern React frontend and a robust FastAPI Python backend. All AI knowledge is served from a managed cloud vector store — no large files live in this repo.

```
Browser  ──HTTPS──►  React + Vite  ──REST/SSE──►  FastAPI  ──►  OpenAI / Gemini / Groq
                                                      │
                                          ┌───────────┴───────────┐
                                       Pinecone             PostgreSQL + Redis
                                    (vector search)       (history + caching)
```

### Frontend

- **Framework:** React 18 with Vite
- **Styling:** Tailwind CSS v4
- **Icons:** Lucide React
- **Animations:** Framer Motion
- **HTTP Client:** Axios

### Backend

- **Framework:** FastAPI
- **AI/LLM:** LangChain, OpenAI, Google Gemini, Groq
- **Vector Store:** Pinecone (cloud-hosted)
- **Database:** PostgreSQL with SQLAlchemy Async & Alembic
- **Caching & Rate Limiting:** Redis, SlowAPI
- **Authentication:** JWT (python-jose, passlib)

---

## 🚀 Getting Started

### Prerequisites

- Node.js v18+
- Python 3.10+
- PostgreSQL (with pgvector extension)
- Redis
- A [Pinecone](https://www.pinecone.io/) account (free tier is sufficient)

### 1. Clone the repository

```bash
git clone https://github.com/BarasaIan11/ESA.git
cd ESA
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

| Variable              | Description                   |
| --------------------- | ----------------------------- |
| `ACTIVE_AI_PROVIDER`  | `openai`, `gemini`, or `groq` |
| `OPENAI_API_KEY`      | OpenAI API key                |
| `GEMINI_API_KEY`      | Google Gemini API key         |
| `GROQ_API_KEY`        | Groq API key                  |
| `PINECONE_API_KEY`    | Pinecone API key              |
| `PINECONE_INDEX_NAME` | Name of your Pinecone index   |
| `DATABASE_URL`        | PostgreSQL connection string  |
| `REDIS_URL`           | Redis connection string       |
| `SECRET_KEY`          | JWT signing secret            |

### 3. Run the backend

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Start the development server
cd backend
uvicorn main:app --reload
```

API is available at `http://localhost:8000`
Auto-generated docs at `http://localhost:8000/docs`

### 4. Run the frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend is available at `http://localhost:5173`

---

## 📚 Knowledge Base Setup

The knowledge base is **not stored in this repository**. Documents are stored in cloud storage and embeddings are hosted on Pinecone. This keeps the repo lightweight and deployable to Vercel/Render without hitting file size limits.

### First-time ingestion

1. Place your Business Central documents (PDFs, DOCX, text files) in a local `knowledge_base/` folder (this folder is gitignored).
2. Run the ingestion script to chunk, embed, and upsert them into Pinecone:

```bash
python scripts/ingest_docs.py
```

3. Re-run this script whenever you add or update documents. Your live deployment will automatically benefit from the updated index — no redeployment needed.

### Recommended documents to index

- Microsoft Learn BC module docs (Finance, Sales, Purchasing, Inventory, Manufacturing)
- Your organisation's SOPs and configuration workbooks
- BC release notes (last 3–4 waves)
- Internal FAQs derived from your helpdesk history
- AL developer and API reference docs
- Known issues and workarounds log

---

## 📁 Project Structure

```
ESA/
├── backend/                  # FastAPI backend
│   ├── main.py               # App entry point
│   ├── config.py             # Environment configuration
│   ├── routers/              # API route handlers
│   │   ├── chat.py           # POST /ask, GET /history
│   │   └── auth.py           # Authentication endpoints
│   ├── services/             # Business logic & AI integration
│   │   ├── ai_gateway.py     # OpenAI / Gemini / Groq abstraction
│   │   ├── prompt_engine.py  # System prompt builder
│   │   ├── retriever.py      # Pinecone vector search
│   │   └── history.py        # Conversation persistence
│   ├── models/               # Database schemas
│   └── middleware/           # CORS, auth, rate limiting
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── components/       # ChatWindow, MessageBubble, InputBar
│   │   ├── api/              # Axios client + SSE helper
│   │   ├── store/            # Zustand session store
│   │   └── types/            # TypeScript definitions
│   └── package.json
├── scripts/
│   └── ingest_docs.py        # Chunk, embed, and upsert docs to Pinecone
├── .env.example              # Environment variable template
├── .gitignore
├── requirements.txt          # Python dependencies
└── README.md

# The following exist locally but are excluded from Git:
# knowledge_base/             Raw BC documents (PDFs, DOCX, etc.)
# vector_db/                  Local vector DB files (no longer used)
# .venv/                      Python virtual environment
# .env                        Secrets and API keys
```

---

## ☁️ Deployment

### Backend — Render / Railway

1. Connect your GitHub repo.
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
4. Add all environment variables from `.env.example` in the dashboard.

### Frontend — Vercel

1. Connect your GitHub repo to Vercel.
2. Set the root directory to `frontend/`.
3. Vercel auto-detects Vite — no extra configuration needed.
4. Add `VITE_API_BASE_URL` pointing to your deployed backend URL.

> The backend should **not** be deployed to Vercel (serverless functions have a 250 MB limit and no persistent connections). Use Render, Railway, or a VPS instead.

---

## 🔒 Security Notes

- Never commit `.env` to Git — it is gitignored by default.
- Rotate your `SECRET_KEY` before going to production.
- The system prompt in `prompt_engine.py` hard-limits ESA to BC topics only — do not remove the guardrails.
- Rate limiting is handled by SlowAPI middleware on the `/ask` endpoint.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Commit your changes: `git commit -m "feat: description"`
4. Push and open a pull request

---

## 📄 License

MIT License — see `LICENSE` for details.
