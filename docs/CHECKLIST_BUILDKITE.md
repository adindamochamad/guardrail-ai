# Checklist Buildkite — bukti sponsor (TODO Day 4 / 7)

**Tutorial lengkap:** [`TUTORIAL_BUILDKITE.md`](TUTORIAL_BUILDKITE.md)  
**Langkah berikutnya (detail pemula):** [`LANGKAH_SELANJUTNYA_BUILDKITE.md`](LANGKAH_SELANJUTNYA_BUILDKITE.md)

Kode integrasi sudah ada; yang dibutuhkan juri adalah **bukti sekali jalan**.

## A. Variabel di VPS (`backend/.env`)

| Variabel | Wajib untuk | Status (21 Mei 2026) |
|----------|-------------|----------------------|
| `BUILDKITE_WEBHOOK_TOKEN` | Verifikasi `POST /webhooks/buildkite` | [x] diisi di VPS |
| `BUILDKITE_API_TOKEN` | Anotasi di UI Buildkite | [ ] isi token API Anda |
| `BUILDKITE_ORG_SLUG` | Slug org (anotasi) | [ ] isi slug org Anda |

Setelah edit: `sudo systemctl restart guardrail-ai`

Uji webhook dari VPS: `./scripts/uji_webhook_buildkite.sh` → harapan **HTTP 200**, `keaslian_webhook: token_ok`.

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

### Smoke lokal (tanpa Buildkite UI) — [x] selesai di VPS

```bash
cd /path/ke/guardrail-ai
GUARDRAIL_URL=https://guardrail-api.adindamochamad.com ./scripts/guardrail_ci_scan.sh
echo "exit: $?"
```

Hasil: **exit 1**, `CRITICAL=3` — lihat [`BUKTI_BUILDKITE.md`](BUKTI_BUILDKITE.md).

Skrip memakai `git -c safe.directory=...` agar aman di VPS.

Pipeline di repo: [`.buildkite/pipeline.yml`](../.buildkite/pipeline.yml) — commit & hubungkan ke Buildkite UI.

## D. Screenshot untuk Devpost

- [ ] Langkah pipeline GuardRail di log build  
- [ ] Build failed + pesan CRITICAL (jika ada)  
- [ ] Anotasi Buildkite (jika webhook + API token aktif)  

## E. Centang di Devpost

Hanya centang **Buildkite** jika A–C minimal **C** selesai.
