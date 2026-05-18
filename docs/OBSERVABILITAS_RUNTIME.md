# Observabilitas runtime (Sentry)

Hud.io saat ini dapat **waitlist** pendaftaran baru. Repo ini menyediakan **integrasi Sentry** sebagai **substitusi praktis** untuk:

- error & exception di FastAPI,
- (opsional) performance tracing bila `SENTRY_TRACES_SAMPLE_RATE` > 0.

Arsitektur sengaja **tipis**: kode ada di `backend/src/observabilitas/` — `fasad.py` memutuskan vendor; `pelaksana_sentry.py` memuat SDK. Nanti Hud.io (atau OpenTelemetry) bisa ditambah paralel tanpa merombak rute API.

## Konfigurasi

Tambahkan ke `backend/.env` (lihat `.env.example`):

| Variabel | Keterangan |
|----------|------------|
| `SENTRY_DSN` | DSN proyek dari dashboard Sentry; **kosong** = tidak aktif |
| `SENTRY_ENVIRONMENT` | Mis. `development`, `staging`, `production` |
| `SENTRY_TRACES_SAMPLE_RATE` | `0.0` (hanya error) sampai `1.0` (semua trace) |
| `SENTRY_DEBUG_ROUTE` | `true` hanya di lokal: mendaftarkan `GET /sentry-debug` untuk mengirim satu error uji |

Di layar **Configure FastAPI SDK**, Sentry menampilkan `sentry_sdk.init(...)` di dalam `main.py`. **Jangan menyalin blok itu** ke proyek ini: inisialisasi sudah ada di `src/observabilitas/` saat startup. Cukup salin **nilai DSN** ke `SENTRY_DSN`.

**Keamanan:** Jika DSN pernah terpapar (chat publik, screenshot), buka **Project Settings → Client Keys** di Sentry, **regenerate** kunci, lalu perbarui `.env`.

**Jangan** commit DSN atau token ke Git.

## Mengetahui status dari API

`GET /health` menyertakan field **`observabilitas_runtime`**:

- `tidak_aktif` — tanpa DSN
- `sentry` — DSN terisi (SDK diinisialisasi saat startup)

## Verifikasi cepat

1. Buat proyek di [sentry.io](https://sentry.io), salin DSN.
2. Set `SENTRY_DSN=...` di `.env`, restart `uvicorn`.
3. Cek `/health` → `observabilitas_runtime` harus `sentry`.
4. (Disarankan) Set `SENTRY_DEBUG_ROUTE=true`, restart server, buka `http://127.0.0.1:8000/sentry-debug` sekali, lalu matikan lagi env itu di produksi. Atau picu error dari kode Anda sendiri. Beberapa detik kemudian cek **Issues** di Sentry.

## Tautan

- Panduan menjalankan backend: [`CARA_JALANKAN_PROYEK.md`](CARA_JALANKAN_PROYEK.md)
- Referensi API: [`API.md`](API.md)
