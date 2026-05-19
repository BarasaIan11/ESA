"""
main.py
-------
FastAPI application entry point.
Registers middleware, routers, and startup/shutdown lifecycle hooks.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from config import settings
from routers import chat, auth


# ── Rate limiter (shared instance) ────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)


# ── Lifespan: startup / shutdown hooks ────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code before `yield` runs on startup.
    Code after `yield` runs on shutdown.
    Add DB pool init, Redis connection, etc. here later.
    """
    print("[ESA] Backend starting up...")
    yield
    print("[ESA] Backend shutting down...")


# ── App factory ───────────────────────────────────────────────────────────────
app = FastAPI(
    title="ESA — ERP Support Assistant",
    description=(
        "AI-powered support assistant specialised in "
        "Microsoft Dynamics 365 Business Central."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# Attach rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",           # local dev
        "https://esa-lac.vercel.app",     # your Vercel URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(chat.router, prefix="/chat", tags=["Chat"])

# ── Root route (Render health check) ──────────────────────────────────────────
@app.get("/", tags=["System"])
async def root():
    """Root route — prevents 404 on Render's health check ping."""
    return {"status": "ESA backend is running"}
# ── Health check ──────────────────────────────────────────────────────────────
@app.get("/health", tags=["System"])
async def health_check():
    """Quick liveness probe — returns 200 if the server is up."""
    return {
        "status": "ok",
        "provider": settings.active_ai_provider,
        "env": settings.app_env,
    }
