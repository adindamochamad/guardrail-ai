# Dashboard GuardRail AI

SPA React (`/scan`): textarea kode, hasil deteksi AI, daftar risiko.

## Prasyarat

- Node.js 20+
- Backend berjalan (lihat [`../backend/README.md`](../backend/README.md))

## Pengembangan

```bash
npm install
# Default memanggil API produksi dari .env.development — ubah bila backend lokal
npm run dev
```

Buka <http://127.0.0.1:5173>.

## Build produksi

```bash
npm run build
```

Artefak di folder `dist/`. Letak tipikal di VPS: `root /var/www/guardrail-ai/frontend/dist` (lihat blok server nginx `guardrail.adindamochamad.com`).

Variabel **`VITE_API_BASE_URL`** (prefix wajib `VITE_`) disematkan pada waktu build. Contoh ada di `.env.production`.

## Backend CORS

API mengizinkan origin:

- Dev Vite: `http://localhost:5173`, `http://127.0.0.1:5173`
- Dashboard: `https://guardrail.adindamochamad.com`

Untuk hostname lain atur **`CORS_ORIGINS`** di `backend/.env` (pisahkan koma).
