# Langkah berikutnya Buildkite — penjelasan detail (untuk pemula)

Anda **sudah menyelesaikan** bagian VPS:

- [x] `BUILDKITE_WEBHOOK_TOKEN`, `BUILDKITE_API_TOKEN`, `BUILDKITE_ORG_SLUG` di `.env`
- [x] `./scripts/uji_webhook_buildkite.sh` → **HTTP 200**, `token_ok`
- [x] `anotasi_terkirim: false` pada skrip uji → **normal** (build #99 tidak ada di Buildkite)

Yang belum: **Buildkite harus menjalankan pipeline sungguhan** di GitHub. Itu yang dijelaskan di bawah.

---

## Gambaran singkat (satu kalimat)

**GitHub** menyimpan resep build (file `.buildkite/pipeline.yml`) → **Buildkite** menarik resep itu → **agent** menjalankan skrip → skrip memanggil **API GuardRail** → kalau ada bug keamanan CRITICAL, build **merah (gagal)**.

---

## Langkah 1 — Push file pipeline ke GitHub (WAJIB dulu)

Di VPS, folder `.buildkite/` **belum** ada di GitHub (hanya di server). Tanpa ini, Buildkite tidak tahu harus jalankan apa.

### 1.1 Cek di VPS

```bash
cd /var/www/guardrail-ai
ls -la .buildkite/pipeline.yml
```

Harus ada file `pipeline.yml`.

### 1.2 Commit & push (jalankan sebagai user yang punya akses git)

```bash
cd /var/www/guardrail-ai
git add .buildkite/pipeline.yml scripts/uji_webhook_buildkite.sh docs/
git status
git commit -m "Tambah pipeline Buildkite dan dokumentasi integrasi."
git push origin main
```

Jika `git push` ditolak, login SSH/token GitHub dulu.

### 1.3 Cek di browser

Buka: `https://github.com/adindamochamad/guardrail-ai/tree/main/.buildkite`

Harus terlihat file **`pipeline.yml`**. Kalau belum ada, ulangi push.

---

## Langkah 2 — Buat pipeline di situs Buildkite

### 2.1 Login

1. Buka https://buildkite.com dan login.
2. Pilih **organisasi** Anda (nama di kiri atas).

### 2.2 Pipeline baru

1. Klik menu **Pipelines** (sidebar kiri).
2. Tombol **New Pipeline** (atau **Create Pipeline**).
3. Pilih sumber **GitHub**.
4. Jika diminta: **Authorize Buildkite** ke GitHub → izinkan akses ke repo `guardrail-ai`.
5. Pilih repository: **`adindamochamad/guardrail-ai`**.
6. **Name** pipeline: ketik misalnya `GuardRail AI` (nama tampilan).
7. Simpan / **Create Pipeline**.

### 2.3 Catat slug pipeline (penting)

Setelah dibuat, buka pipeline tersebut. Lihat **URL** di browser, contoh:

```text
https://buildkite.com/guardrail-ai/pipelines/guardrail-ai
                              ^^^^^^^^^^^          ^^^^^^^^^^^
                              org slug             pipeline slug
```

- **Org slug** harus sama dengan `BUILDKITE_ORG_SLUG` di `.env` Anda.
- **Pipeline slug** (bagian terakhir) — catat di kertas, misalnya `guardrail-ai`.

Slug ini dipakai saat webhook mengirim anotasi; kalau beda, anotasi tidak muncul (404).

---

## Langkah 3 — Tambah secret `GUARDRAIL_URL`

Secret = password/URL rahasia yang hanya agent Buildkite yang tahu.

1. Masih di halaman pipeline → tab **Settings** (pipeline, bukan organisasi).
2. Cari menu **Environment Variables** atau **Secrets**.
3. Klik **New Variable** / **Add**.
4. Isi:

| Field | Nilai |
|--------|--------|
| Key / Name | `GUARDRAIL_URL` |
| Value | `https://guardrail-api.adindamochamad.com` |
| Secret? | Centang **Yes** / **Hidden** jika ada opsi |

5. Simpan.

Tanpa ini, skrip di pipeline memanggil `localhost` dan gagal aneh.

---

## Langkah 4 — Jalankan build pertama

### 4.1 Trigger build

1. Di halaman pipeline, tombol **New Build** (kanan atas).
2. **Branch:** pilih `main` (pastikan branch `main` sudah punya `.buildkite/pipeline.yml` dari Langkah 1).
3. **Commit:** biarkan default (terbaru).
4. Klik **Create Build** / **Build**.

### 4.2 Tunggu agent

- Buildkite butuh **agent** (mesin yang menjalankan perintah). Akun baru biasanya pakai **hosted agents** Buildkite atau Anda pasang agent sendiri.
- Jika build status **Waiting for agent** lama: di **Agent Settings** organisasi, pastikan ada agent online (atau aktifkan hosted agents di plan Anda).

### 4.3 Baca hasil (yang diharapkan untuk demo)

Buka build → lihat daftar **Steps**:

| Yang Anda inginkan | Artinya |
|--------------------|---------|
| Step **`:shield: GuardRail — scan risiko`** berwarna **merah / failed** | GuardRail menemukan CRITICAL → **sukses untuk hackathon** |
| Log berisi `guardrail_ci_scan: gagal` dan `CRITICAL=` | Bukti untuk screenshot Devpost |

**Jangan panik jika build gagal** — untuk repo `guardrail-ai` ini **memang dirancang gagal** karena ada pola `eval`/`exec` di kode Python yang dipindai.

Jika step **hijau**: cek log — mungkin `GUARDRAIL_URL` salah atau tidak ada file `.py` terlacak.

### 4.4 Screenshot (untuk Devpost)

Ambil 2 gambar:

1. Daftar step dengan step GuardRail **merah**.
2. Zoom log: baris `guardrail_ci_scan: gagal` dan angka `CRITICAL`.

---

## Langkah 5 — Webhook (agar anotasi muncul di build)

Ini **langkah terpisah** dari pipeline. Anda sudah uji webhook dari VPS (200 OK). Sekarang hubungkan Buildkite → VPS.

### 5.1 Buat notification webhook

1. Di Buildkite, pilih **organisasi** (bukan satu pipeline).
2. **Settings** (organisasi) → **Notification Services**.
3. **Add notification service** → **Webhook**.
4. Isi:

| Field | Nilai |
|--------|--------|
| URL | `https://guardrail-api.adindamochamad.com/webhooks/buildkite` |
| Token | Buka di VPS: `sudo grep BUILDKITE_WEBHOOK_TOKEN /var/www/guardrail-ai/backend/.env` — salin nilai setelah `=` (jangan share ke publik) |

5. Simpan.

### 5.2 Trigger build lagi

Setelah build **selesai** (pass atau fail), Buildkite mengirim event ke VPS.

1. Jalankan **New Build** lagi (Langkah 4).
2. Buka build yang sama → tab **Annotations** (atau **Anotasi**).
3. Jika berhasil: ada catatan markdown **GuardRail AI — hasil pemindaian**.

Jika tab kosong:

- Pastikan webhook tidak error 401 di **Notification Services** → **Deliveries**.
- Pastikan `BUILDKITE_ORG_SLUG` di `.env` = org di URL Buildkite.
- Build harus **benar-benar ada** (bukan build #99 fiktif dari skrip uji).

---

## Langkah 6 — Centang di Devpost

Setelah **Langkah 4** selesai (satu build dengan step GuardRail, meski merah):

- [ ] Centang challenge / sponsor **Buildkite** di formulir Devpost.
- [ ] Lampirkan screenshot build gagal + URL API `https://guardrail-api.adindamochamad.com/docs`.

---

## Troubleshooting

| Masalah | Apa yang dilakukan |
|---------|---------------------|
| Tidak ada step GuardRail di build | File `.buildkite/pipeline.yml` belum di GitHub → Langkah 1 |
| `Waiting for agent` | Pasang / nyalakan Buildkite agent |
| Step gagal `curl: (6) Could not resolve host` | Secret `GUARDRAIL_URL` salah atau kosong → Langkah 3 |
| Step gagal `HTTP 502` | API VPS restart; tunggu 10 detik, build ulang |
| Webhook 401 di Buildkite | Token webhook UI ≠ `BUILDKITE_WEBHOOK_TOKEN` di `.env` |
| Anotasi kosong | Normal sampai build nyata + webhook Langkah 5; cek slug org/pipeline |
| Skrip uji `anotasi_terkirim: false` | Normal — build #99 tidak ada di Buildkite |

---

## Urutan yang benar (checklist)

```
[ ] 1. Push .buildkite/pipeline.yml ke GitHub
[ ] 2. Buat pipeline di buildkite.com + hubungkan repo
[ ] 3. Secret GUARDRAIL_URL di pipeline Settings
[ ] 4. New Build → screenshot step merah
[ ] 5. (Opsional) Webhook organisasi + build lagi → cek Annotations
[ ] 6. Devpost
```

---

## Butuh bantuan dari agent/Cursor

Kirim pesan misalnya: *"Tolong commit dan push .buildkite ke GitHub"* — tanpa perlu menempel token.

Dokumen terkait: [`TUTORIAL_BUILDKITE.md`](TUTORIAL_BUILDKITE.md), [`CHECKLIST_BUILDKITE.md`](CHECKLIST_BUILDKITE.md).
