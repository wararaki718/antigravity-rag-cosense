import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.sparse_encoder import encode_text, get_encoder

logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Pre-load the SPLADE model at startup."""
    logger.info("Pre-loading SPLADE model...")
    get_encoder()
    logger.info("Encoder service ready")
    yield


app = FastAPI(
    title="Sparse Encoder API",
    description="SPLADE sparse vector encoding service using japanese-splade",
    version="0.1.0",
    lifespan=lifespan,
)


class EncodeRequest(BaseModel):
    text: str


class EncodeResponse(BaseModel):
    vector: dict[str, float]


@app.get("/api/health")
async def health_check() -> dict:
    return {"status": "ok", "service": "encoder"}


@app.post("/api/encode", response_model=EncodeResponse)
async def encode(request: EncodeRequest) -> EncodeResponse:
    """Encode text to a sparse vector."""
    try:
        vector = encode_text(request.text)
        return EncodeResponse(vector=vector)
    except Exception as e:
        logger.error(f"Encoding failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
