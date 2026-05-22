# Bukti Buildkite (Fase B1)

Dokumen ini mencatat uji yang sudah dijalankan di VPS **21 Mei 2026**. Screenshot UI Buildkite tetap perlu Anda ambil setelah langkah manual di bawah.

## C. Smoke pipeline (blokir CRITICAL) — selesai

Perintah:

```bash
cd /var/www/guardrail-ai
GUARDRAIL_URL=https://guardrail-api.adindamochamad.com ./scripts/guardrail_ci_scan.sh
echo "exit: $?"
```

Hasil:

| Item | Nilai |
|------|--------|
| HTTP `/scan` | 200 |
| Ringkasan | `CRITICAL=3`, `HIGH=6`, `LOW=73` |
| Exit code | **1** (gagal sesuai desain — ada CRITICAL) |
| Durasi | ~3 menit (repo penuh, `gunakan_llm: false`) |

Contoh temuan CRITICAL di log: `GR_SEC_EVAL_001`, `GR_SEC_EXEC_001` (cuplikan `eval(` / `exec(` di berkas Python terlacak Git).

**Kesimpulan:** langkah pipeline Buildkite akan **merah** saat memindai repo ini — cocok untuk demo “GuardRail memblokir merge”.

## A. Variabel VPS — sebagian

| Variabel | Status |
|----------|--------|
| `BUILDKITE_WEBHOOK_TOKEN` | **Diisi** (generated 48 char hex) di `backend/.env` |
| `BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED` | `false` |
| `BUILDKITE_API_TOKEN` | **Kosong** — anotasi UI Buildkite belum aktif |
| `BUILDKITE_ORG_SLUG` | **Kosong** — isi slug org Anda (mis. `acme-corp`) |

Setelah mengisi `BUILDKITE_API_TOKEN` + `BUILDKITE_ORG_SLUG`: `sudo systemctl restart guardrail-ai`

## B. Webhook — backend diverifikasi, UI Buildkite perlu Anda

Uji VPS (`./scripts/uji_webhook_buildkite.sh`):

| Item | Nilai |
|------|--------|
| HTTP | 200 |
| `keaslian_webhook` | `token_ok` |
| `anotasi_terkirim` | false (API token belum diisi) |
| Ringkasan pesan commit uji | `HIGH: 1` |

1. Buildkite → **Notification Services** → **Webhook**
2. URL: `https://guardrail-api.adindamochamad.com/webhooks/buildkite`
3. Token: sama dengan `BUILDKITE_WEBHOOK_TOKEN` di `backend/.env` (jangan commit / jangan paste di chat publik)
4. Trigger satu build → screenshot log webhook / anotasi

Uji otomatis dari VPS (setelah token di `.env`):

```bash
./scripts/uji_webhook_buildkite.sh
```

## Pipeline di repo

- [`/.buildkite/pipeline.yml`](../.buildkite/pipeline.yml) — langkah `guardrail-scan`
- Secret Buildkite: `GUARDRAIL_URL=https://guardrail-api.adindamochamad.com`

Hubungkan repo `adindamochamad/guardrail-ai` ke pipeline Buildkite, lalu jalankan build pada branch `main`.

## D. Screenshot Devpost (checklist)

- [ ] Log langkah `:shield: GuardRail — scan risiko`
- [ ] Build **failed** + baris `guardrail_ci_scan: gagal`
- [ ] Anotasi Buildkite (setelah `BUILDKITE_API_TOKEN` + webhook UI)

## E. Devpost

Centang challenge **Buildkite** setelah minimal **C** + satu build nyata di UI (disarankan juga **B**).
