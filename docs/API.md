# API GuardRail AI — referensi (Day 5)

Base URL lokal: `http://127.0.0.1:8000`

| Metode | Path        | Deskripsi |
|--------|-------------|-----------|
| `GET`  | `/health`   | Status layanan (`status`, `service`, `observabilitas_runtime`: `tidak_aktif` \| `sentry`). |
| `GET`  | `/db/ping`  | Sambungan ORM + jumlah baris `scans` dan `code_files`. |
| `POST` | `/detect`   | Deteksi heuristik kode hasil AI (pola + metadata Git + LLM opsional). |
| `POST` | `/analyze`  | Analisis risiko: **30+ aturan regex** + **11 pemeriksaan AST** (Python). |
| `POST` | `/scan`     | **Deteksi lalu analisis** — label AI dari deteksi diteruskan ke analisis. |
| `POST` | `/webhooks/buildkite` | Webhook pipeline Buildkite: verifikasi, pemindaian, anotasi opsional. |

Dokumentasi OpenAPI: `/docs` (Swagger UI) dan `/openapi.json`.

Observabilitas runtime (Sentry): [`OBSERVABILITAS_RUNTIME.md`](OBSERVABILITAS_RUNTIME.md).

---

## `POST /detect`

Lihat contoh di versi sebelumnya; body: `kode`, `pesan_commit?`, `gunakan_llm?`.

---

## `POST /analyze`

**Body JSON**

| Field | Tipe | Default | Keterangan |
|-------|------|---------|------------|
| `kode` | string | — | Cuplikan kode (wajib). |
| `bahasa` | string | `python` | `python`, `javascript`, `typescript`, atau lain (`universal` saja). |
| `apakah_ai` | bool / null | `null` | Jika `null`, **inferensi** via `deteksi_ai` (tanpa LLM). |
| `lewati_aturan_khusus_ai_jika_bukan_ai` | bool | `true` | Abaikan aturan bertanda *khusus AI* bila kode dianggap manusia. |

**Respons (inti)**

- `daftar_temuan`: `{ id_aturan, kategori, tingkat_keparahan, nomor_baris, deskripsi, saran_perbaikan?, cuplikan?, dari_ast }`
- `jumlah_temuan`, `ringkasan_keparahan`, `apakah_ai_inferensi`, `apakah_ai_efektif`, `bahasa`

---

## `POST /scan`

Gabungan **`/detect`** + **`/analyze`**. Mewarisi field `PermintaanDeteksi` (`kode`, `pesan_commit`, `gunakan_llm`) plus:

| Field | Tipe | Default | Keterangan |
|-------|------|---------|------------|
| `bahasa` | string | `python` | Sama seperti `/analyze`. |
| `apakah_ai` | bool / null | `null` | Jika `null`, pakai **hasil** `deteksi.apakah_ai` untuk filter aturan AI. |
| `lewati_aturan_khusus_ai_jika_bukan_ai` | bool | `true` | Sama seperti `/analyze`. |

**Respons**

- `deteksi`: sama seperti balasan `/detect`
- `analisis`: sama seperti balasan `/analyze`
- `jumlah_total_aturan_sistem`: jumlah aturan bawaan (regex + jenis AST) untuk metadata produk

---

## CI Buildkite (blokir build)

Untuk **menghentikan pipeline** bila ada temuan CRITICAL (bukan hanya anotasi webhook), gunakan langkah yang memanggil **`POST /scan`**. Panduan dan contoh YAML: [`BUILDKITE_PIPELINE.md`](BUILDKITE_PIPELINE.md).

---

## `POST /webhooks/buildkite`

Menerima **body mentah** JSON event Buildkite (sama seperti yang dikirim ke URL webhook).

**Header (satu dari)**

- `X-Buildkite-Token`: harus sama dengan `BUILDKITE_WEBHOOK_TOKEN`, atau
- `X-Buildkite-Signature`: `timestamp=...,signature=...` (HMAC-SHA256 hex atas `{timestamp}.{body utf-8}`).

**Tanpa** `BUILDKITE_WEBHOOK_TOKEN`: respons **503** kecuali `BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED=true` (hanya dev).

**Alur**

1. Verifikasi keaslian.
2. Parse JSON; jalankan deteksi AI + analisis pada **pesan commit** (default) atau cuplikan dari **git clone ringkas** jika `BUILDKITE_WEBHOOK_GIT_CLONE=true`.
3. Jika `BUILDKITE_API_TOKEN` + metadata build/pipeline/org lengkap → kirim **anotasi** ke API Buildkite v2.

**Respons** (inti)

- `deteksi`, `analisis` — sama konsepnya dengan `/scan`
- `keaslian_webhook`, `x_buildkite_event`
- `anotasi_terkirim`, `anotasi_status_http`, `anotasi_error` (jika gagal)
- `peringatan` bila tidak ada teks untuk dipindai

---

## Variabel lingkungan (backend)

- `AI_DETECT_THRESHOLD` — deteksi AI (default `0.55`).
- `OPENAI_API_KEY` / `OPENAI_MODEL` — untuk `gunakan_llm: true` pada `/detect` dan `/scan`.
- `BUILDKITE_WEBHOOK_TOKEN` — verifikasi webhook.
- `BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED` — izinkan webhook tanpa rahasia (dev).
- `BUILDKITE_API_TOKEN` — Bearer untuk anotasi build.
- `BUILDKITE_ORG_SLUG` — slug organisasi bawaan (opsional; payload biasanya sudah berisi `organization.slug`).
- `BUILDKITE_WEBHOOK_GIT_CLONE` / `BUILDKITE_GIT_DEPTH` — opsi klon ringkas saat webhook.
- `SENTRY_DSN` / `SENTRY_ENVIRONMENT` / `SENTRY_TRACES_SAMPLE_RATE` — observabilitas runtime (opsional).

---

## Rencana (Day 6+)

- Dashboard hasil scan.
- Integrasi CI tambahan.
