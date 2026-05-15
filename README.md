# ESA — ERP Support Assistant

ESA is an AI-powered support assistant specialized in Microsoft Dynamics 365 Business Central. It provides a conversational interface for users to ask questions, troubleshoot issues, and get guidance on using Business Central effectively.

## 🏗 Architecture

The project is structured as a monorepo containing a modern React frontend and a robust FastAPI Python backend.

### Frontend
- **Framework:** React 18 with Vite
- **Styling:** Tailwind CSS v4
- **Icons:** Lucide React
- **Animations:** Framer Motion
- **HTTP Client:** Axios

### Backend
- **Framework:** FastAPI
- **AI/LLM:** LangChain, OpenAI, Google Gemini, Groq
- **Vector Store:** FAISS, pgvector (PostgreSQL), Pinecone, ChromaDB
- **Database:** PostgreSQL (with SQLAlchemy Async & Alembic)
- **Caching & Rate Limiting:** Redis, SlowAPI
- **Authentication:** JWT (python-jose, passlib)

## 🚀 Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.10+)
- PostgreSQL (with pgvector extension)
- Redis

### Environment Variables
Copy `.env.example` to `.env` in the root directory and configure your API keys and database connections:

```bash
cp .env.example .env
```

Key variables to configure:
- `ACTIVE_AI_PROVIDER` (openai, gemini, or groq)
- API Keys (`OPENAI_API_KEY`, `GEMINI_API_KEY`, `GROQ_API_KEY`)
- `DATABASE_URL` (PostgreSQL connection string)
- `REDIS_URL`

### Running the Backend

1. Navigate to the root directory and activate your virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI development server:
```bash
cd backend
uvicorn main:app --reload
```
The API will be available at `http://localhost:8000`. API documentation is auto-generated at `http://localhost:8000/docs`.

### Running the Frontend

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the Vite development server:
```bash
npm run dev
```
The frontend will be available at `http://localhost:5173`.

## 📁 Project Structure

```
ESA/
├── backend/            # FastAPI backend application
│   ├── main.py         # App entry point
│   ├── config.py       # Environment configuration
│   ├── routers/        # API endpoints
│   ├── models/         # Database models
│   ├── services/       # Business logic & AI integration
│   └── middleware/     # Custom middleware
├── frontend/           # React frontend application
│   ├── src/
│   │   ├── components/ # Reusable UI components
│   │   ├── api/        # Axios API clients
│   │   ├── store/      # State management
│   │   └── types/      # TypeScript definitions
│   └── package.json
├── knowledge_base/     # Raw documentation and data for RAG
├── vector_db/          # Local vector database storage (if using ChromaDB)
├── scripts/            # Utility scripts (e.g., data ingestion)
├── requirements.txt    # Python dependencies
└── .env                # Environment variables
```
