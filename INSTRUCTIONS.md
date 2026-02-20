# RAG Application - Cosense + Elasticsearch

## Project Overview
Cosense のデータを SPLADE スパースベクトルで Elasticsearch に格納し、Ollama (Gemma3) で回答を生成する RAG アプリケーション。

## Tech Stack
- **Backend API**: Python 3.11+ / FastAPI (port 8000) — 検索 + LLM 回答生成
- **Encoder API**: Python 3.11+ / FastAPI (port 8001) — SPLADE スパースベクトル変換
- **Batch**: Python 3.11+ — Cosense からのデータ取り込み
- **Frontend**: TypeScript / React (Vite)
- **Search**: Elasticsearch 8.17.0 (sparse_vector)
- **Embedding**: hotchpotch/japanese-splade-v2 (via yasem)
- **LLM**: Ollama / Gemma3
- **Infra**: Docker Compose

## Architecture
3つの独立したPythonプロジェクト:
- `backend/` — 検索 API。encoder API を呼んでクエリをベクトル化し、ES で検索、Ollama で回答生成。
- `encoder/` — スパースベクトル変換 API。japanese-splade モデルを保持。backend と batch から共有利用。
- `batch/` — バッチ取り込み。Cosense API → encoder API → Elasticsearch。

## Coding Conventions
- Python の型ヒントを使用。async/await を活用。
- TypeScript strict mode。関数コンポーネント + hooks。
- 環境変数は `.env` で管理し、`pydantic-settings` で読み込む。
- Elasticsearch クライアントのメジャーバージョンは ES と合わせる (8.x)。

## Directory Structure
```
backend/          — FastAPI search API (port 8000)
  app/            — Application code
  tests/          — Tests
encoder/          — FastAPI encoder API (port 8001)
  app/            — Application code
batch/            — Batch ingestion
  app/            — Application code
frontend/         — React frontend
  src/            — Source code
docker-compose.yml — Elasticsearch + Ollama
```
