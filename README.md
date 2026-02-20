# Cosense RAG

Cosense のナレッジベースを AI で検索する RAG (Retrieval-Augmented Generation) アプリケーション。

## Architecture

```
┌──────────┐    ┌──────────────┐    ┌──────────────┐    ┌───────────────┐
│ Frontend │───▶│ Backend :8000│───▶│ Encoder :8001│    │ Ollama Gemma3 │
│ React    │◀───│ FastAPI      │◀───│ SPLADE       │    │ :11434        │
└──────────┘    │              │───▶│              │    │               │
                │              │◀───└──────────────┘    │               │
                │              │───▶┌──────────────┐    │               │
                │              │◀───│Elasticsearch │    │               │
                │              │    │ :9200        │    │               │
                │              │───▶│              │    │               │
                │              │◀───└──────────────┘    │               │
                │              │───────────────────────▶│               │
                │              │◀───────────────────────│               │
                └──────────────┘                        └───────────────┘

┌────────────┐    ┌──────────────┐    ┌──────────────┐
│ Cosense API│───▶│ Batch        │───▶│ Encoder :8001│
│            │◀───│ Ingestion    │◀───│              │
└────────────┘    │              │───▶└──────────────┘
                  │              │───▶┌──────────────┐
                  │              │    │Elasticsearch │
                  └──────────────┘    └──────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | TypeScript / React (Vite) |
| Backend API | Python / FastAPI |
| Encoder API | Python / FastAPI + japanese-splade-v2 |
| Batch | Python CLI |
| Search | Elasticsearch 8.17.0 (sparse_vector) |
| LLM | Ollama / Gemma3:1b |
| Infra | Docker Compose |

## Directory Structure

```
backend/           # 検索 API (port 8000)
encoder/           # スパースベクトル変換 API (port 8001)
batch/             # Cosense → Elasticsearch バッチ取り込み
frontend/          # React UI
docker-compose.yml # Elasticsearch + Ollama
```

## Setup

### 1. 環境変数

```bash
cp .env.example .env
```

### 2. Docker 起動

```bash
docker compose up -d
docker exec rag-ollama ollama pull gemma3:1b
```

### 3. Python 環境 (各プロジェクト)

```bash
# Encoder
cd encoder && python -m venv .venv && source .venv/bin/activate && pip install -e .

# Backend
cd backend && python -m venv .venv && source .venv/bin/activate && pip install -e .

# Batch
cd batch && python -m venv .venv && source .venv/bin/activate && pip install -e .
```

### 4. Frontend

```bash
cd frontend && npm install
```

## Usage

### 開発サーバー起動

```bash
# 1. Encoder (port 8001)
cd encoder && source .venv/bin/activate && uvicorn app.main:app --reload --port 8001

# 2. Backend (port 8000)
cd backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000

# 3. Frontend (port 5173)
cd frontend && npm run dev
```

### データ取り込み

```bash
cd batch && source .venv/bin/activate && python -m app.ingest
```

## License

See [LICENSE](./LICENSE).