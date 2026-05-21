# Cara menjalankan proyek GuardRail AI

Panduan ini mencakup **backend FastAPI** (`backend/`), **frontend dashboard** (`frontend/`), dan **cek verifikasi** (`make qa`). Untuk struktur besar proyek, lihat [`README.md`](../README.md).

---

## Prasyarat

- **Python 3.11** atau lebih baru (**3.12** boleh)
- **Node.js 18+** (disarankan **20.19+** jika Anda nanti meningkatkan stack Vite; di VPS beberapa image memakai 20.18 dengan Vite 5 dan berjalan baik setelah downgrade toolchain)
- **Git**
- Opsional: kunci **OpenAI** untuk `gunakan_llm: true`; **Buildkite** untuk uji webhook; **Sentry** (`SENTRY_*`); subdomain publik Anda sendiri seperti contoh **`guardrail-api` / `guardrail`** (bukan wajib untuk lokal)

---

## 1. Clone repo

```bash
git clone https://github.com/adindamochamad/guardrail-ai.git
cd guardrail-ai
```

Sesuaikan URL kalau Anda memakai fork atau remote lain.

---

## 2. Backend (`backend/`)

### 2.1 Virtual environment

Di repo ini venv direkomendasikan di **`backend/.venv`** (folder titik):

```bash
cd backend
python3 -m venv .venv
```

**Aktivasi**

- Linux / macOS:

  ```bash
  source .venv/bin/activate
  ```

- Windows (PowerShell): `\.venv\Scripts\Activate.ps1`

Pasang dependensi:

```bash
python -m pip install -r requirements.txt
```

> Jika dokumentasi Anda lama menyebut `venv/` tanpa titik — ganti ke **`source .venv/bin/activate`**.

### 2.2 File `.env`

```bash
cp .env.example .env
chmod 600 .env   # disarankan
```

Sesuaikan (jangan meng-commit rahasia):

| Variabel | Keterangan |
|----------|------------|
| `DATABASE_URL` | Default SQLite `./guardrail.db` relatif ke **cwd saat uvicorn berjalan** (idealnya dari folder `backend/`) |
| `OPENAI_API_KEY` / `OPENAI_MODEL` | Opsional — LLM di `/detect` & `/scan` |
| `BUILDKITE_*` | Webhook + anotasi — lihat [`docs/API.md`](API.md), [`BUILDKITE_PIPELINE.md`](BUILDKITE_PIPELINE.md) |
| `SENTRY_*` | Observabilitas produksi (`docs/OBSERVABILITAS_RUNTIME.md`) |
| `CORS_ORIGINS` | Origin tambahan (koma); bawaan kode mencakup `localhost:5173` dan dashboard `guardrail.adindamochamad.com` — sesuaikan domain Anda |

### 2.3 Menjalankan API **lokal (dev)**

Dari **`backend/`** dengan `.venv` aktif:

```bash
cd backend
source .venv/bin/activate
# Hindari bentrok dengan layanan lain di port 8000 di mesin Anda; contoh pakai 8010:
uvicorn src.main:app --reload --host 127.0.0.1 --port 8010
```

**Pemisah perintah:** `source …/activate` dan baris **`uvicorn`** harus lengkap secara terpisah (jangan menyambung seperti `activateuvicorn`).

- **Swagger lokal:** <http://127.0.0.1:8010/docs>
- **`/health`:** <http://127.0.0.1:8010/health>

Contoh **`curl`** (sesuaikan port):

```bash
curl -s http://127.0.0.1:8010/health
```

Catatan **`Makefile`:** target `make run-backend` mem-bind **localhost** pada port **8010** (lihat `Makefile` akar repo) agar pola port tidak bentrok cepat dengan angka lain; ubah satu tempat kalau Anda mau konsisten lain.

---

## 3. Frontend dashboard (`frontend/`)

### 3.1 Ketergantungan

```bash
cd frontend
npm install
```

Variabel **`VITE_API_BASE_URL`** (tanpa slash akhir) di-set pada waktu **`npm run build`** lewat **`frontend/.env.production`**. Untuk pengembangan, **`frontend/.env.development`** mengarahkan ke URL API default produksi Anda — ubah misalnya ke **`http://127.0.0.1:8010`** kalau Anda hanya tes lokal tanpa HTTPS.

### 3.2 Dev server (hot reload)

```bash
npm run dev
```

Biasanya <http://127.0.0.1:5173>. Backend harus mengizinkan **CORS** dari origin tersebut (sudah diatur di kode untuk dev).

### 3.3 Build produksi (hasil statis `dist/`)

```bash
npm run build
```

Folder **`frontend/dist`** di-deploy seperti biasa SPA (mis. nginx **`root`** + `try_files … /index.html`). Contoh produksi Anda: subdomain dashboard HTTPS terpisah dari API dengan origin yang sama daftar izin CORS production.

Referensi cepat: [`frontend/README.md`](../frontend/README.md).

---

## 4. Satu pintu — verifikasi (`make qa`) dari akar repo

Gabungan lint backend, tes, dan **build frontend** (jika `frontend/node_modules` ada):

```bash
cd guardrail-ai
make qa
# alias:
make verify
```

Rincian: [`docs/AGENSI_VERIFIKASI_QA.md`](AGENSI_VERIFIKASI_QA.md). Agensi QA ini juga digunakan oleh hook Cursor (**`stop`**) secara opsional ketika Anda bekerja di IDE yang mendukungnya.

Makefile lain:

| Target | Fungsi |
|--------|--------|
| `make install` | `pip install -r backend/requirements.txt` (gunakan venv Anda sendiri) |
| `make lint` | Ruff dari folder `backend/` |
| `make test` | Pytest cepat dari folder `backend/` |
| `make run-backend` | Uvicorn reload (lihat Makefile untuk `--host/--port`) |

---

## 5. Contoh memanggil API (CLI)

Sesuaikan **host/port** atau URL publik Anda.

```bash
# Deteksi
curl -s -X POST http://127.0.0.1:8010/detect \
  -H 'Content-Type: application/json' \
  -d '{"kode":"def hello():\n    pass"}' | python3 -m json.tool

# Analisis
curl -s -X POST http://127.0.0.1:8010/analyze \
  -H 'Content-Type: application/json' \
  -d '{"kode":"eval(\"1+1\")","bahasa":"python"}' | python3 -m json.tool

# Gabungan MVP
curl -s -X POST http://127.0.0.1:8010/scan \
  -H 'Content-Type: application/json' \
  -d '{"kode":"import os\nos.system(\"echo hi\")","bahasa":"python"}' | python3 -m json.tool
```

Referensi lengkap: [`docs/API.md`](API.md).

---

## 6. Contoh lingkungan **produksi** (orientasi VPS + nginx — ilustratif)

Sesuaikan nama host dan path dengan server Anda sendiri:

| Peran | Contoh subdomain | Penjelasan ringkas |
|-------|-------------------|---------------------|
| API | `https://guardrail-api.<domain>/docs` | Reverse proxy nginx → **`127.0.0.1:8008`** (contoh systemd; port lain boleh asal konsisten) |
| SPA | `https://guardrail.<domain>` | `root …/frontend/dist`, `try_files` untuk SPA |
| systemd | Layanan **`guardrail-ai`** | `WorkingDirectory=/path/.../guardrail-ai/backend`, jalankan **`uvicorn src.main:app`** di **localhost** pada port Anda |

Versi aplikasi (**OpenAPI**): **v0.6.0** (cek `backend/src/main.py`).

Ini **bukan** petunjuk copy-paste server; dokumentasi infra detail tetap bersifat internal organisasi Anda.

---

## 7. Masalah umum

| Gejala | Penyebab / solusi cepat |
|--------|--------------------------|
| `venv/bin/activate: No such file` | Anda memakai path salah — gunakan **`source .venv/bin/activate`** dari `backend/`. |
| `Address already in use` untuk uvicorn | Port dipakai proses lain (mis. **8000** sering bentrok dengan stack lain pada satu VPS) — pakai **`--port 8010`** atau **`8008`** dan satu sumber kebenaran di nginx/systemd Anda. |
| Dashboard tidak bisa panggil API (CORS) | Pastikan **`Origin`** hostname dashboard Anda ada di whitelist kode (**`config.py`**) dan/atau variabel **`CORS_ORIGINS`**. |
| `make qa` tidak build frontend | **Tidak ada** `frontend/node_modules` → jalankan **`npm install`** di **`frontend/`** dulu (perilaku yang disengaja agar VPS tanpa Node tidak gagal sia-sia). |
| Webhook Buildkite | Lihat **`BUILDKITE_*`** dan [`docs/API.md`](API.md) — jangan menghidupkan **`BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED`** di production. |

---

## 8. Dokumen lain

| Berkas |
|--------|
| [`TODO.md`](../TODO.md) — checklist hackathon yang disinkron dengan realitas repo |
| [`backend/README.md`](../backend/README.md) |
| [`docs/API.md`](API.md) |
| [`docs/BUILDKITE_PIPELINE.md`](BUILDKITE_PIPELINE.md) |
| [`docs/OBSERVABILITAS_RUNTIME.md`](OBSERVABILITAS_RUNTIME.md) |

---

_Informasi jalankan-local terakhir dibandingkan dengan kondisi repo: backend **v0.6.0**, frontend Vite/React di **`frontend/`**, dan **`make qa` aktif._
