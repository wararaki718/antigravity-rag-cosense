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

### 1. 初期セットアップ

`Makefile` を使用して、環境変数の作成、ビルド、起動をまとめて行います。

```bash
make setup
```

※ 個別に実行する場合:
```bash
cp -n .env.example .env
docker compose build
docker compose up -d
```

### 2. LLM モデルのダウンロード

初回のみ実行が必要です。

```bash
make pull-model
```

## Usage

### サービスの確認

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Encoder API**: [http://localhost:8001/docs](http://localhost:8001/docs)

### データ取り込み (Batch)

Cosense からデータを取得し、Elasticsearch にインデックスします。

```bash
make ingest
```

### 便利コマンド

```bash
make logs    # ログの確認
make ps      # コンテナの状態確認
make down    # サービスの停止
```

## License

See [LICENSE](./LICENSE).