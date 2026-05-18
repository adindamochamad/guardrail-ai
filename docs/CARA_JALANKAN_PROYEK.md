# Cara menjalankan proyek GuardRail AI

Panduan ini menjelaskan cara menjalankan **backend FastAPI** dari nol hingga API siap dipakai. Frontend dashboard belum tersedia di repo ini; fokus saat ini adalah API di folder `backend/`.

---

## Prasyarat

- **Python 3.11** atau lebih baru
- **Git** (untuk meng-clone repo)
- Terminal (macOS/Linux: `bash`/`zsh`; Windows: PowerShell atau Git Bash)

Opsional:

- Kunci **OpenAI** jika ingin memakai mode LLM pada endpoint deteksi (`gunakan_llm: true`)
- Akun **Buildkite** jika ingin menguji webhook CI

---

## 1. Clone dan masuk ke folder proyek

```bash
git clone https://github.com/<organisasi-atau-user>/guardrail-ai.git
cd guardrail-ai
```

Sesuaikan URL clone dengan repo Anda.

---

## 2. Persiapan backend

Semua perintah berikut dijalankan dari folder **`backend/`**.

### 2.1 Buat virtual environment dan pasang dependensi

```bash
cd backend
python3 -m venv venv
```

**Aktivasi venv** (wajib di setiap sesi terminal baru):

- **macOS / Linux:**

  ```bash
  source venv/bin/activate
  ```

- **Windows (cmd):**

  ```bat
  venv\Scripts\activate.bat
  ```

- **Windows (PowerShell):**

  ```powershell
  .\venv\Scripts\Activate.ps1
  ```

Lalu pasang paket:

```bash
python -m pip install -r requirements.txt
```

### 2.2 File lingkungan (`.env`)

```bash
cp .env.example .env
```

Edit `.env` sesuai kebutuhan. Minimal untuk jalan lokal biasanya cukup default SQLite. Variabel yang sering disentuh:

| Variabel | Keterangan |
|----------|------------|
| `DATABASE_URL` | Default: `sqlite:///./guardrail.db` (relatif ke cwd saat menjalankan uvicorn dari `backend/`) |
| `OPENAI_API_KEY` | Opsional; untuk deteksi dengan LLM |
| `OPENAI_MODEL` | Misalnya `gpt-4o-mini` |
| `BUILDKITE_*` | Lihat [`backend/README.md`](../backend/README.md) / [`docs/API.md`](API.md) untuk webhook Buildkite |

> **Jangan** meng-commit berkas `.env` yang berisi rahasia.

---

## 3. Menjalankan server API

Pastikan venv **sudah aktif** dan Anda berada di folder **`backend/`**.

```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --reload
```

**Penting:** `source venv/bin/activate` dan `uvicorn ...` adalah **dua perintah terpisah** (boleh dua baris, atau satu baris dengan `&&`). Jangan digabung jadi `source .../activateuvicorn` — itu tidak valid.

### Opsi host dan port

Bind ke semua interface (berguna untuk akses dari mesin lain / kontainer):

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 4. Cara dari root repo (Makefile)

Jika Anda berada di **root** `guardrail-ai/` (bukan di dalam `backend/`):

```bash
make install      # pip install -r backend/requirements.txt
make run-backend  # uvicorn dengan --host 0.0.0.0 --port 8000
make test         # pytest di backend
make lint         # ruff di backend
```

Perintah `make run-backend` tidak mengaktifkan venv secara otomatis. Pastikan `python` dan `uvicorn` yang dipakai mengarah ke environment yang sudah terpasang dependensi (biasanya setelah `cd backend && source venv/bin/activate` sekali, atau set PATH Anda ke `backend/venv`).

---

## 5. Memastikan API berjalan

Setelah server hidup, buka di browser:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

Contoh dengan `curl`:

```bash
curl -s http://127.0.0.1:8000/health
```

---

## 6. Contoh memanggil endpoint utama

Deteksi AI singkat:

```bash
curl -s -X POST http://127.0.0.1:8000/detect \
  -H "Content-Type: application/json" \
  -d '{"kode":"def hello():\n    pass"}' | python3 -m json.tool
```

Analisis risiko:

```bash
curl -s -X POST http://127.0.0.1:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"kode":"eval(\"1+1\")","bahasa":"python"}' | python3 -m json.tool
```

Deteksi lalu analisis (alur gabungan):

```bash
curl -s -X POST http://127.0.0.1:8000/scan \
  -H "Content-Type: application/json" \
  -d '{"kode":"import os\nos.system(\"echo hi\")","bahasa":"python"}' | python3 -m json.tool
```

Referensi lengkap field request/response: [`docs/API.md`](API.md).

---

## 7. Menjalankan tes dan linter

Dari folder **`backend/`** dengan venv aktif:

```bash
pytest -q
ruff check src tests
```

---

## 8. Masalah yang sering muncul

| Gejala | Kemungkinan penyebab |
|--------|----------------------|
| `ModuleNotFoundError` / tidak ada `uvicorn` | venv belum diaktifkan atau `pip install` belum dijalankan di venv yang sama |
| Salah database / path SQLite | Pastikan menjalankan `uvicorn` dari folder **`backend/`** agar path `sqlite:///./guardrail.db` konsisten |
| Port 8000 sudah dipakai | Ganti port: `uvicorn src.main:app --reload --port 8001` |
| Webhook Buildkite 401/503 | Cek `BUILDKITE_WEBHOOK_TOKEN` dan/atau `BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED` (hanya dev); lihat [`docs/API.md`](API.md) |

---

## 9. Dokumen terkait

- [`backend/README.md`](../backend/README.md) — ringkasan backend, Buildkite, tes
- [`docs/API.md`](API.md) — referensi endpoint
- [`docs/BUILDKITE_PIPELINE.md`](BUILDKITE_PIPELINE.md) — contoh pipeline Buildkite + pemblokiran CRITICAL
- [`docs/OBSERVABILITAS_RUNTIME.md`](OBSERVABILITAS_RUNTIME.md) — Sentry (error & trace opsional)
- [`README.md`](../README.md) — visi proyek dan arsitektur tingkat tinggi
