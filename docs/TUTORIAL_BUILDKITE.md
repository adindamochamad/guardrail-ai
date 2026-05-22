# Tutorial Buildkite — step by step (GuardRail AI)

Panduan ini untuk **Fase B1 hackathon**: membuktikan integrasi Buildkite (pipeline gagal saat CRITICAL + webhook opsional).

**Yang sudah jalan di VPS Anda (tidak perlu ulang):**

- API: `https://guardrail-api.adindamochamad.com`
- `BUILDKITE_WEBHOOK_TOKEN` sudah diisi di `backend/.env`
- Smoke scan: exit **1** (ada CRITICAL) — GuardRail memblokir build

**Yang Anda lakukan di browser Buildkite + beberapa baris di VPS.**

---

## Gambaran dua jalur

| Jalur | Apa yang terjadi | Wajib untuk Devpost? |
|--------|------------------|----------------------|
| **Pipeline** (`guardrail_ci_scan.sh`) | Agent Buildkite memanggil `POST /scan` → step **merah** jika CRITICAL | **Ya** (minimal ini) |
| **Webhook** (`POST /webhooks/buildkite`) | Setelah build selesai, Buildkite kirim event → GuardRail kirim **anotasi** di UI | Disarankan (lebih kaya demo) |

---

## Prasyarat

1. Akun [Buildkite](https://buildkite.com) (gratis untuk open source / trial).
2. Repo GitHub: `https://github.com/adindamochamad/guardrail-ai` — akses untuk menghubungkan ke Buildkite.
3. SSH ke VPS (atau editor di server) untuk edit `backend/.env`.
4. Di laptop/agent Buildkite: `curl`, `jq`, `git`, `bash` (image Linux default biasanya sudah ada).

---

## Bagian 1 — Siapkan token di VPS (5 menit)

### Langkah 1.1 — Buka file environment

```bash
sudo -u guardrail nano /var/www/guardrail-ai/backend/.env
```

(Atau `vim` / editor di Cursor.)

### Langkah 1.2 — Pastikan baris Buildkite seperti ini

| Variabel | Nilai | Keterangan |
|----------|--------|------------|
| `BUILDKITE_WEBHOOK_TOKEN` | **Sudah terisi** di VPS | Jangan ganti kecuali Anda juga ganti token di UI Buildkite |
| `BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED` | `false` | Wajib di produksi |
| `BUILDKITE_API_TOKEN` | Token dari Buildkite (langkah 2) | Untuk anotasi di halaman build |
| `BUILDKITE_ORG_SLUG` | Slug organisasi Anda | Contoh: `my-startup` (lihat URL Buildkite) |

**Cara tahu `BUILDKITE_ORG_SLUG`:** buka Buildkite → organisasi Anda → URL biasanya `https://buildkite.com/<slug-org>/...`

### Langkah 1.3 — Restart backend

```bash
sudo systemctl restart guardrail-ai
sudo systemctl status guardrail-ai --no-pager
curl -sS https://guardrail-api.adindamochamad.com/health | head -c 200
```

Harapan: service **active**, health JSON berisi `"ok": true` (atau setara).

### Langkah 1.4 — Uji webhook dari VPS (opsional tapi cepat)

```bash
cd /var/www/guardrail-ai
./scripts/uji_webhook_buildkite.sh
```

| Hasil | Artinya |
|--------|---------|
| `HTTP 200` + `keaslian_webhook: token_ok` | Backend siap terima webhook |
| `HTTP 401` | Token di Buildkite UI ≠ token di `.env` |
| `HTTP 503` | `BUILDKITE_WEBHOOK_TOKEN` kosong atau service belum restart |

Setelah mengisi `BUILDKITE_API_TOKEN`, jalankan lagi — `anotasi_terkirim` bisa `true` hanya jika build nyata + metadata lengkap (bagian 3).

---

## Bagian 2 — Token API Buildkite (untuk anotasi)

### Langkah 2.1 — Buat API Access Token

1. Login [buildkite.com](https://buildkite.com).
2. Klik avatar (kanan atas) → **Personal Settings** (atau **Organization Settings** → API Access Tokens, tergantung tipe akun).
3. **API Access Tokens** → **New Token**.
4. Beri nama misalnya `guardrail-ai-vps`.
5. Scope minimal: akses **read/write** untuk organisasi dan pipelines (ikut petunjuk UI saat membuat token).
6. Salin token **sekali** — tempel ke `BUILDKITE_API_TOKEN=` di `backend/.env`.
7. `sudo systemctl restart guardrail-ai`.

---

## Bagian 3 — Webhook di UI Buildkite

### Langkah 3.1 — Buka Notification Services

1. Pilih **organisasi** Anda di Buildkite.
2. Menu **Settings** (organisasi) → **Notification Services**.
3. **Add notification service** → pilih **Webhook**.

### Langkah 3.2 — Isi webhook

| Field | Nilai |
|--------|--------|
| **Webhook URL** | `https://guardrail-api.adindamochamad.com/webhooks/buildkite` |
| **Token** | Salin persis dari `BUILDKITE_WEBHOOK_TOKEN` di `backend/.env` |
| **Events** | Biarkan default yang mengirim event build (mis. build finished) |

Simpan.

### Langkah 3.3 — Verifikasi

- Jalankan **satu build** (bagian 4 dulu jika pipeline belum ada).
- Di log build atau di halaman notification, cek tidak ada error 401 ke URL GuardRail.
- Di VPS: `./scripts/uji_webhook_buildkite.sh` sudah membuktikan backend; webhook UI membuktikan Buildkite → VPS.

**Screenshot untuk Devpost:** halaman notification / delivery webhook sukses, atau anotasi GuardRail di tab build.

---

## Bagian 4 — Hubungkan repo GitHub ke Buildkite

### Langkah 4.1 — Buat pipeline baru

1. Organisasi → **Pipelines** → **New Pipeline**.
2. Pilih **GitHub** → authorize jika diminta.
3. Pilih repository **`guardrail-ai`** (user `adindamochamad`).
4. Pipeline name: misalnya `guardrail-ai` (slug akan dipakai di webhook/anotasi).

### Langkah 4.2 — Pastikan file pipeline ada di repo

Di GitHub harus ada:

```text
.buildkite/pipeline.yml
scripts/guardrail_ci_scan.sh
```

Jika belum di-push dari VPS:

```bash
cd /var/www/guardrail-ai
git status
# commit & push .buildkite/, scripts/, docs/ sesuai kebutuhan Anda
```

Isi pipeline (sudah di repo):

```yaml
steps:
  - label: ":shield: GuardRail — scan risiko (blokir jika CRITICAL)"
    key: guardrail-scan
    commands:
      - chmod +x scripts/guardrail_ci_scan.sh
      - export GUARDRAIL_URL="${GUARDRAIL_URL:-https://guardrail-api.adindamochamad.com}"
      - ./scripts/guardrail_ci_scan.sh
```

Buildkite otomatis membaca `.buildkite/pipeline.yml` dari branch yang di-build.

### Langkah 4.3 — Tambah secret `GUARDRAIL_URL`

1. Buka pipeline **guardrail-ai** → **Settings** → **Environment** (atau **Secrets**).
2. Tambah variabel:

| Nama | Nilai |
|------|--------|
| `GUARDRAIL_URL` | `https://guardrail-api.adindamochamad.com` |

Tanpa trailing slash `/`.

### Langkah 4.4 — Trigger build pertama

1. **New Build** pada branch `main` (atau branch yang sudah berisi `.buildkite/pipeline.yml`).
2. Tunggu agent menjalankan step `:shield: GuardRail — scan risiko`.

**Hasil yang diharapkan untuk demo hackathon:**

- Step **gagal** (merah).
- Log berisi baris seperti:
  - `guardrail_ci_scan: memanggil https://guardrail-api.../scan`
  - `ringkasan keparahan: {"CRITICAL":3,...}`
  - `guardrail_ci_scan: gagal — ada temuan pada ambang CRITICAL`

Ini **bukan bug** — repo berisi pola `eval`/`exec` di berkas Python terlacak Git; GuardRail sengaja memblokir.

**Screenshot Devpost:**

1. Daftar step pipeline dengan step GuardRail merah.
2. Cuplikan log dengan `CRITICAL` dan `guardrail_ci_scan: gagal`.
3. (Opsional) Tab **Annotations** setelah webhook + API token aktif.

---

## Bagian 5 — Smoke test tanpa UI Buildkite

Berguna sebelum / sesudah setup UI:

```bash
cd /var/www/guardrail-ai
GUARDRAIL_URL=https://guardrail-api.adindamochamad.com ./scripts/guardrail_ci_scan.sh
echo "exit: $?"
```

Atau:

```bash
make buildkite-smoke
make buildkite-webhook
```

| `exit` | Artinya |
|--------|---------|
| `0` | Tidak ada CRITICAL (atau tidak ada `.py` terlacak) |
| `1` | Ada CRITICAL → pipeline Buildkite harus gagal |
| `2` | `curl`/`jq`/bukan repo git |

---

## Bagian 6 — Centang Devpost & narasi juri

1. Centang sponsor **Buildkite** hanya jika minimal **satu build nyata** dengan step GuardRail (bagian 4).
2. Jangan centang **Hud.io** tanpa integrasi SDK nyata.
3. Di teks submission, sebutkan:
   - URL API: `https://guardrail-api.adindamochamad.com/docs`
   - Pipeline memanggil `/scan` dan **gagal pada CRITICAL**
   - Webhook + anotasi (jika bagian 3 selesai)

Draf teks: [`DEVPOST_DRAFT.md`](DEVPOST_DRAFT.md).

---

## Troubleshooting

| Gejala | Penyebab umum | Solusi |
|--------|----------------|--------|
| Webhook `401` | Token UI ≠ `.env` | Samakan `BUILDKITE_WEBHOOK_TOKEN`, restart service |
| Webhook `503` | Token kosong | Isi token, `BUILDKITE_WEBHOOK_ALLOW_UNVERIFIED=false` |
| Step gagal `curl: command not found` | Agent minimal | Pakai image Linux standar Buildkite |
| Step gagal `jq: command not found` | Sama | Install `jq` di hook/agent atau ganti image |
| HTTP `/scan` timeout | Repo besar (~3 menit) | Normal; naikkan timeout step di pipeline jika perlu |
| Build hijau padahal harus merah | Secret `GUARDRAIL_URL` salah | Cek secret mengarah ke API produksi |
| Anotasi tidak muncul | `BUILDKITE_API_TOKEN` kosong / slug salah | Isi API token + `BUILDKITE_ORG_SLUG`, restart |
| `git dubious ownership` di VPS | Ownership repo | Sudah ditangani di skrip via `safe.directory` |

---

## Checklist cepat (centang sendiri)

- [ ] `BUILDKITE_WEBHOOK_TOKEN` di `.env` (sudah di VPS)
- [ ] `BUILDKITE_API_TOKEN` + `BUILDKITE_ORG_SLUG` di `.env`
- [ ] `sudo systemctl restart guardrail-ai`
- [ ] `./scripts/uji_webhook_buildkite.sh` → HTTP 200
- [ ] Webhook di Buildkite Notification Services
- [ ] Repo terhubung + `.buildkite/pipeline.yml` di GitHub
- [ ] Secret `GUARDRAIL_URL` di pipeline
- [ ] Satu build di UI → step GuardRail **merah**
- [ ] 2–3 screenshot untuk Devpost
- [ ] Centang Buildkite di Devpost

---

## Dokumen terkait

| File | Isi |
|------|-----|
| [`CHECKLIST_BUILDKITE.md`](CHECKLIST_BUILDKITE.md) | Checklist singkat |
| [`BUKTI_BUILDKITE.md`](BUKTI_BUILDKITE.md) | Hasil uji VPS |
| [`BUILDKITE_PIPELINE.md`](BUILDKITE_PIPELINE.md) | Webhook vs pipeline (teknis) |
| [`API.md`](API.md) | Kontrak `/webhooks/buildkite` dan `/scan` |
