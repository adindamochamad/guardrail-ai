# Backend GuardRail AI (Day 1–4)

## Prasyarat

- Python **3.11+**

## Fitur API (ringkas)

| Path | Fungsi |
|------|--------|
| `GET /health` | Smoke check |
| `GET /db/ping` | Cek ORM |
| `POST /detect` | Deteksi kode AI |
| `POST /analyze` | Aturan risiko + AST Python |
| `POST /scan` | Deteksi → analisis (alur demo) |
| `POST /webhooks/buildkite` | Webhook Buildkite + anotasi opsional |

Detail: [`docs/API.md`](../docs/API.md).

## Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env
```

## Menjalankan API

Dari folder `backend/`:

```bash
uvicorn src.main:app --reload
```

- Dokumentasi interaktif: http://127.0.0.1:8000/docs  
- `GET /health`, `GET /db/ping`, `POST /detect`, `POST /analyze`, `POST /scan`, `POST /webhooks/buildkite` — lihat [`docs/API.md`](../docs/API.md)

## Buildkite (ringkas)

1. Set `BUILDKITE_WEBHOOK_TOKEN` (dan untuk anotasi: `BUILDKITE_API_TOKEN`; opsional `BUILDKITE_ORG_SLUG`).
2. Di Buildkite, tambahkan **Notification Service** → **Webhook** menuju `https://<host-anda>/webhooks/buildkite`.
3. Untuk dev lokal tanpa token, **jangan** dipakai di produksi: `BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED=true`.

## Tes & lint

```bash
cd backend
pytest -q
ruff check src tests
```

Atau dari root repo: `make test`, `make lint`.

## Catatan

- Saat startup, aplikasi memanggil `create_all` untuk SQLite dev. Produksi sebaiknya memakai migrasi (Alembic) — direncanakan di fase berikutnya.
- Tes memaksa `DATABASE_URL=sqlite:///:memory:` lewat `tests/conftest.py` agar tidak menulis berkas lokal.
- Modul deteksi: `src/ai_detector/` — pola statis (21+), metadata commit, OpenAI opsional.
- Modul analisis: `src/analisis_risiko/` — ≥30 aturan regex + pemeriksaan AST Python.
- Integrasi Buildkite: `src/integrasi_buildkite/` — verifikasi webhook, pemindaian, klien anotasi REST.
