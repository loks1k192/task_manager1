.PHONY: help install run test lint format docker-up docker-down migrate clean

help: ## Показать справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Установить зависимости
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run: ## Запустить приложение
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Запустить тесты
	pytest -v

test-cov: ## Запустить тесты с покрытием
	pytest --cov=app --cov-report=term-missing --cov-report=html

lint: ## Проверить код линтером
	ruff check .
	mypy app

format: ## Отформатировать код
	ruff format .
	ruff check --fix .

docker-up: ## Запустить Docker контейнеры
	docker-compose up -d

docker-down: ## Остановить Docker контейнеры
	docker-compose down

docker-logs: ## Показать логи Docker контейнеров
	docker-compose logs -f

migrate: ## Применить миграции
	alembic upgrade head

migrate-create: ## Создать новую миграцию (использовать: make migrate-create MESSAGE="описание")
	alembic revision --autogenerate -m "$(MESSAGE)"

migrate-downgrade: ## Откатить последнюю миграцию
	alembic downgrade -1

clean: ## Очистить временные файлы
	find . -type d -name __pycache__ -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
