import sys
import os
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Ensure project root is available
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.routes.analysis import router as analysis_router
from api.routes.documents import router as documents_router
from api.routes.evaluation import router as evaluation_router

app = FastAPI(
    title="ThreatRAG API",
    description=(
        "Production-grade research API for ThreatRAG: An Adaptive Hybrid "
        "Retrieval-Augmented Generation Framework for Explainable Cybersecurity "
        "Threat Intelligence and Incident Response."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for web dashboards and local clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Process timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    return response


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error in ThreatRAG service",
            "detail": str(exc),
            "path": str(request.url.path)
        }
    )


# Health checks
@app.get("/", tags=["Health"])
@app.get("/health", tags=["Health"])
@app.get("/api/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "ThreatRAG API",
        "version": "1.0.0",
        "architecture": "Adaptive Hybrid RAG + Calibrated Multi-Agent Orchestration",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
    }


# Include endpoint routers
app.include_router(analysis_router)
app.include_router(documents_router)
app.include_router(evaluation_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host="127.0.0.1", port=8000, reload=False)
