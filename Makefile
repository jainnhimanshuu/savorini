.PHONY: help up down build test lint clean db.migrate db.reset seed

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

up: ## Start all services
	docker-compose up -d
	@echo "🚀 Services starting..."
	@echo "   Backend API: http://localhost:8000/docs"
	@echo "   Vendor Portal: http://localhost:3000"
	@echo "   Admin Console: http://localhost:3001"
	@echo "   Mobile (Expo): http://localhost:8081"

down: ## Stop all services
	docker-compose down

build: ## Build all containers
	docker-compose build

test: ## Run all tests
	docker-compose exec backend pytest
	docker-compose exec web-vendor npm test
	docker-compose exec web-admin npm test
	docker-compose exec mobile npm test

lint: ## Run linting
	docker-compose exec backend ruff check . && black --check .
	docker-compose exec web-vendor npm run lint
	docker-compose exec web-admin npm run lint
	docker-compose exec mobile npm run lint

clean: ## Clean containers and volumes
	docker-compose down -v
	docker system prune -f

db.migrate: ## Run database migrations
	docker-compose exec backend alembic upgrade head

db.reset: ## Reset database (DESTRUCTIVE)
	docker-compose down -v
	docker-compose up -d postgres redis
	sleep 5
	docker-compose exec backend alembic upgrade head

seed: ## Load seed data
	docker-compose exec backend python -m ops.scripts.seed

logs: ## View logs
	docker-compose logs -f

shell.backend: ## Backend shell
	docker-compose exec backend bash

shell.db: ## Database shell
	docker-compose exec postgres psql -U postgres -d happyhour

dev.backend: ## Run backend in dev mode
	cd apps/backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000

dev.vendor: ## Run vendor portal in dev mode
	cd apps/web-vendor && npm run dev

dev.admin: ## Run admin console in dev mode
	cd apps/web-admin && npm run dev

dev.mobile: ## Run mobile app in dev mode
	cd apps/mobile && npx expo start
