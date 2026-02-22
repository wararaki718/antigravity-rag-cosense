.PHONY: build up down logs ps ingest setup pull-model help

# Default target
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  setup      Copy .env.example to .env and start everything"
	@echo "  build      Build or rebuild services"
	@echo "  up         Create and start containers"
	@echo "  down       Stop and remove containers"
	@echo "  logs       Fetch the logs of all services"
	@echo "  ps         List containers"
	@echo "  ingest     Run the batch ingestion process"
	@echo "  pull-model Pull the Ollama model (gemma3:1b)"

setup:
	@if [ ! -f .env ]; then cp .env.example .env; fi
	docker compose build
	docker compose up -d
	@echo "Setup complete. Don't forget to run 'make pull-model' if this is your first time."

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

ps:
	docker compose ps

ingest:
	docker compose run --rm batch python -m app.ingest

pull-model:
	docker exec rag-ollama ollama pull gemma3:1b
