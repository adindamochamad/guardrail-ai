# Agensi verifikasi & QA GuardRail AI

Gabungan satu perintah untuk **lint backend**, **tes pytest**, dan **build produksi frontend** — dipakai manusia, CI, serta hook Cursor setelah satu siklus agent.

## Jalankan cepat

Dari akar repo `guardrail-ai/`:

```bash
make qa
```

Setara:

```bash
bash scripts/agensi_verifikasi_qa.sh
```

## Tahapan di dalam skrip

| Tahap           | Lokasi           | Perilaku                                                 |
|-----------------|------------------|----------------------------------------------------------|
| Ruff            | `backend/`       | `ruff check src tests`                                   |
| Pytest          | `backend/`       | `pytest -q`                                              |
| Build frontend | `frontend/`      | `npm run build` jika `node_modules/` ada               |

Preferensi interpreter: **`backend/.venv/bin/ruff`** dan **`backend/.venv/bin/pytest`** bila ada.

## Hook Cursor (`stop`)

- Berkas konfigurasi: [`.cursor/hooks.json`](../.cursor/hooks.json)
- Skrip: [`.cursor/hooks/jalankan-qa-stop.sh`](../.cursor/hooks/jalankan-qa-stop.sh)
- Log gabungan hook + keluaran skrip QA: `.cursor/qa-setelah-agent-terakhir.log`

Hook memaksa **timeout panjang** (hingga ~10 menit) agar build frontend sempat selesai. Keluarannya **tidak diblok** ke pengguna utama di chat; pantau bilah **Hooks** / Channel Hooks di Cursor bila gagal atau baca log di atas.

Aktifasi: simpan repo, buka lagi proyek; bila tidak jalan **restart Cursor** (perilaku dokumentasi Cursor untuk `hooks.json`).

## Cursor Agent Rule

Rule **always-applied** [.cursor/rules/agensi-verifikasi-qa.mdc](../.cursor/rules/agensi-verifikasi-qa.mdc) menyuruh AI menjalankan `make qa` dan melaporkan hasil secara eksplisit.

## Frontend pertama kali

```bash
cd frontend && npm install && npm run build
```

Tanpa `node_modules`, langkah frontend pada agensi QA dilewati dengan pesan (supaya VPS tanpa Node tidak gagal sia-sia).

## Menambahkan langkah baru (mis. E2E)

Edit [`scripts/agensi_verifikasi_qa.sh`](../scripts/agensi_verifikasi_qa.sh) dan dokumentasikan di README ini serta di `Makefile` target `qa`.
