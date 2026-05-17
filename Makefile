# Perintah umum GuardRail AI (jalankan dari root repo)

.PHONY: help install lint test run-backend

help:
	@echo "Perintah:"
	@echo "  make install     - pip install backend (dev)"
	@echo "  make lint        - ruff check backend"
	@echo "  make test        - pytest backend"
	@echo "  make run-backend - jalankan uvicorn reload"

install:
	cd backend && python -m pip install -r requirements.txt

lint:
	cd backend && ruff check src tests

test:
	cd backend && pytest -q

run-backend:
	cd backend && uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
