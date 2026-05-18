# Buildkite: webhook vs pemblokiran build

GuardRail punya dua jalur di CI:

| Jalur | Fungsi |
|--------|--------|
| **Webhook** `POST /webhooks/buildkite` | Setelah build, Buildkite mengirim event → anotasi di UI (butuh `BUILDKITE_API_TOKEN`, dll.). Tidak menghentikan pipeline secara otomatis. |
| **Langkah pipeline** | Agent memanggil API **`/scan`** (atau skrip di bawah) dengan kode di checkout. Jika ada temuan **CRITICAL** (opsional **HIGH**), proses keluar dengan **kode ≠ 0** → Buildkite menandai langkah gagal dan Anda bisa memblokir merge. |

Dokumentasi API: [`API.md`](API.md). Panduan menjalankan server: [`CARA_JALANKAN_PROYEK.md`](CARA_JALANKAN_PROYEK.md).

---

## Prasyarat di agent

- `curl`, `jq`, `git`, `bash`
- Jaringan dari agent ke host GuardRail (URL publik atau jaringan internal)
- Repositori yang dipindai sudah di-checkout (biasanya `$BUILDKITE_BUILD_CHECKOUT_PATH`)

---

## Skrip siap pakai: `scripts/guardrail_ci_scan.sh`

Skrip menggabungkan berkas `*.py` yang terlacak Git (menghindari `venv/`, `.venv/`, `node_modules/`), memanggil **`POST /scan`**, lalu:

- **Gagal (exit 1)** jika `analisis.ringkasan_keparahan.CRITICAL > 0`
- Jika `GUARDRAIL_FAIL_SEVERITY=HIGH`, gagal juga bila ada temuan **HIGH**

### Variabel lingkungan

| Nama | Default | Keterangan |
|------|---------|------------|
| `GUARDRAIL_URL` | `http://127.0.0.1:8000` | Base URL API **tanpa** trailing `/` |
| `GUARDRAIL_FAIL_SEVERITY` | `CRITICAL` | `CRITICAL` saja, atau `HIGH` untuk ikut memblokir HIGH |
| `GUARDRAIL_MAX_CHARS` | `450000` | Potongan gabungan kode sebelum kirim (di bawah batas body API) |

### Menjalankan lokal (smoke)

Dari root repo, dengan API hidup di mesin yang sama:

```bash
chmod +x scripts/guardrail_ci_scan.sh
GUARDRAIL_URL=http://127.0.0.1:8000 ./scripts/guardrail_ci_scan.sh
```

### Buildkite (secret)

Simpan URL produksi dan token OpenAI (jika nanti dipakai) sebagai **secret** Buildkite, misalnya:

- `GUARDRAIL_URL` → `https://guardrail.contoh.com`

---

## Contoh definisi pipeline

Lihat berkas **`buildkite/guardrail-pipeline.example.yml`** di repo ini. Salin ke pipeline Buildkite Anda dan sesuaikan:

- `GUARDRAIL_URL` (secret)
- cabang / trigger
- plugin/agent yang dipakai

---

## Urutan yang disarankan

1. Pipeline menjalankan langkah **GuardRail** setelah checkout (misalnya setelah unit test cepat).
2. Jika langkah gagal, developer melihat log + daftar temuan (skrip mencetak cuplikan `daftar_temuan` ke stderr).
3. **Webhook** tetap berguna untuk **anotasi** ringkas di halaman build tanpa menggantikan langkah gagal di atas.

---

## Batasan

- Skrip mengirim **cuplikan** berkas Python terlacak hingga batas karakter; monorepo sangat besar mungkin perlu strategi lain (pemindaian per-paket, artefak, atau endpoint khusus).
- Deteksi LLM di CI biasanya dimatikan (`gunakan_llm: false` di skrip) agar stabil dan tanpa biaya per commit.
