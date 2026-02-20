import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import settings
from app.encoder_client import EncoderClient
from app.es_client import ESClient
from app.llm_client import generate_answer

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

es_client: ESClient | None = None
encoder_client: EncoderClient | None = None


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manage application lifecycle."""
    global es_client, encoder_client
    es_client = ESClient()
    encoder_client = EncoderClient()
    logger.info("Application started")
    yield
    if es_client:
        es_client.close()
    if encoder_client:
        encoder_client.close()
    logger.info("Application shutdown")


app = FastAPI(
    title="RAG Cosense API",
    description="RAG search API using sparse vector search and LLM answer generation",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Request / Response Models ---


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class SourceDocument(BaseModel):
    title: str
    source_url: str
    score: float


class SearchResponse(BaseModel):
    answer: str
    sources: list[SourceDocument]
    query: str


# --- Endpoints ---


@app.get("/api/health")
async def health_check() -> dict:
    """Health check endpoint."""
    return {
        "status": "ok",
        "elasticsearch_url": settings.elasticsearch_url,
        "ollama_model": settings.ollama_model,
        "encoder_url": settings.encoder_url,
    }


@app.post("/api/search", response_model=SearchResponse)
async def search(request: SearchRequest) -> SearchResponse:
    """Search for relevant documents and generate an answer."""
    if not es_client or not encoder_client:
        raise HTTPException(status_code=503, detail="Service not initialized")

    try:
        # 1. Encode query to sparse vector via encoder API
        logger.info(f"Encoding query: {request.query}")
        query_vector = encoder_client.encode(request.query)

        # 2. Search Elasticsearch
        logger.info(f"Searching with top_k={request.top_k}")
        results = es_client.search(query_vector, top_k=request.top_k)

        if not results:
            return SearchResponse(
                answer="関連するドキュメントが見つかりませんでした。",
                sources=[],
                query=request.query,
            )

        # 3. Generate answer with LLM
        logger.info(f"Generating answer from {len(results)} results")
        answer = generate_answer(request.query, results)

        # 4. Build response
        sources = [
            SourceDocument(
                title=r["title"],
                source_url=r["source_url"],
                score=r["score"],
            )
            for r in results
        ]

        return SearchResponse(
            answer=answer,
            sources=sources,
            query=request.query,
        )

    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
