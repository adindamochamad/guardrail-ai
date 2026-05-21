# Perintah umum GuardRail AI (jalankan dari root repo)

.PHONY: help install lint test qa verify run-backend

help:
	@echo "Perintah:"
	@echo "  make install     - pip install backend (dev)"
	@echo "  make lint        - ruff check backend"
	@echo "  make test        - pytest backend"
	@echo "  make qa / verify - agensi QA (ruff + pytest + npm run build frontend bila ada node_modules)"
	@echo "  make run-backend - uvicorn reload (sesuaikan port di host Anda; ada bentrok pada :8000)"

install:
	cd backend && python -m pip install -r requirements.txt

lint:
	cd backend && ruff check src tests

test:
	cd backend && pytest -q

verify: qa

qa:
	@bash scripts/agensi_verifikasi_qa.sh

run-backend:
	cd backend && uvicorn src.main:app --reload --host 127.0.0.1 --port 8010
