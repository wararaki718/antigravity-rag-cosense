---
description: Run data ingestion from Cosense into Elasticsearch
---

// turbo-all

1. Ensure Elasticsearch is running:
```bash
curl -s http://localhost:9200/_cluster/health | grep -q '"status":"green"\|"status":"yellow"' && echo "ES is ready" || echo "ES is not running - run /dev first"
```

2. Ensure the encoder service is running:
```bash
curl -s http://localhost:8001/api/health | grep -q '"status":"ok"' && echo "Encoder is ready" || echo "Encoder is not running - run /dev first"
```

3. Run the ingestion script:
```bash
cd /Users/wararaki/workspace/antigravity-rag-cosense/batch && source .venv/bin/activate && python -m app.ingest
```

4. Verify document count:
```bash
curl -s http://localhost:9200/cosense_pages/_count | python -m json.tool
```
