---
description: Start the development environment (Docker + Backend + Frontend)
---

// turbo-all

1. Start Docker containers (Elasticsearch + Ollama):
```bash
cd /Users/wararaki/workspace/antigravity-rag-cosense && docker compose up -d
```

2. Wait for Elasticsearch to be healthy:
```bash
until curl -s http://localhost:9200/_cluster/health | grep -q '"status":"green"\|"status":"yellow"'; do sleep 2; done && echo "Elasticsearch is ready"
```

3. Pull Gemma3 model in Ollama (if not already pulled):
```bash
docker exec rag-ollama ollama pull gemma3:1b
```

4. Start the encoder service (port 8001):
```bash
cd /Users/wararaki/workspace/antigravity-rag-cosense/encoder && source .venv/bin/activate && uvicorn app.main:app --reload --port 8001
```

5. Start the backend API server (port 8000):
```bash
cd /Users/wararaki/workspace/antigravity-rag-cosense/backend && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000
```

6. Start the frontend dev server (in a new terminal):
```bash
cd /Users/wararaki/workspace/antigravity-rag-cosense/frontend && npm run dev
```
