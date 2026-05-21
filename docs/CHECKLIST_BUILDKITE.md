# Checklist Buildkite — bukti sponsor (TODO Day 4 / 7)

Kode integrasi sudah ada; yang dibutuhkan juri adalah **bukti sekali jalan**.

## A. Variabel di VPS (`backend/.env`)

| Variabel | Wajib untuk |
|----------|-------------|
| `BUILDKITE_WEBHOOK_TOKEN` | Verifikasi `POST /webhooks/buildkite` |
| `BUILDKITE_API_TOKEN` | Anotasi di UI Buildkite |
| `BUILDKITE_ORG_SLUG` | Opsional jika slug tidak ada di payload |

Setelah edit: `sudo systemctl restart guardrail-ai`

## B. Webhook Buildkite

1. Buildkite → **Notification Services** → **Webhook**  
2. URL: `https://guardrail-api.adindamochamad.com/webhooks/buildkite`  
3. Token sama dengan `BUILDKITE_WEBHOOK_TOKEN`  
4. Trigger satu build → screenshot anotasi atau log webhook di Buildkite  

## C. Pipeline — blokir merge (disarankan untuk demo)

1. Salin [`buildkite/guardrail-pipeline.example.yml`](../buildkite/guardrail-pipeline.example.yml)  
2. Secret Buildkite: `GUARDRAIL_URL=https://guardrail-api.adindamochamad.com`  
3. Pastikan repo memuat `scripts/guardrail_ci_scan.sh` (sudah di repo)  
4. Jalankan build pada branch uji dengan cuplikan Python berisiko → step **merah** jika ada CRITICAL  

### Smoke lokal (tanpa Buildkite UI)

```bash
cd /path/ke/guardrail-ai
GUARDRAIL_URL=https://guardrail-api.adindamochamad.com ./scripts/guardrail_ci_scan.sh
echo "exit: $?"
```

Skrip memakai `git -c safe.directory=...` agar aman di VPS.

## D. Screenshot untuk Devpost

- [ ] Langkah pipeline GuardRail di log build  
- [ ] Build failed + pesan CRITICAL (jika ada)  
- [ ] Anotasi Buildkite (jika webhook + API token aktif)  

## E. Centang di Devpost

Hanya centang **Buildkite** jika A–C minimal **C** selesai.
