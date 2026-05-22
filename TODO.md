# GuardRail AI - TODO Checklist

Versi backend: **v0.6.0**

---

## Urutan kerja (ikuti ini)

### Fase A — TODO internal (dokumen & alat) ← **kerjakan dulu**

| # | Item | Status |
|---|------|--------|
| A1 | Dokumentasi jalankan (`CARA_JALANKAN_PROYEK.md`) | [x] |
| A2 | Sinkron `TODO.md` + prioritas | [x] |
| A3 | Skrip eval deteksi + `backend/tests/fixtures_eval_deteksi.json` + `docs/HASIL_EVAL_DETEKSI.md` | [x] |
| A4 | Draf Devpost `docs/DEVPOST_DRAFT.md` | [x] |
| A5 | Checklist Buildkite `docs/CHECKLIST_BUILDKITE.md` | [x] |
| A6 | Perbaiki `guardrail_ci_scan.sh` (git safe.directory VPS) | [x] |
| A7 | `make qa` hijau | [x] |
| A8 | Commit + push ke GitHub | [x] |

### Fase B — Peluang menang hackathon ← **setelah Fase A**

| # | Item | Status | Dampak |
|---|------|--------|--------|
| B1 | **Buildkite bukti nyata** — smoke + webhook backend selesai; UI Buildkite + `BUILDKITE_API_TOKEN` oleh Anda | [~] | Sponsor Buildkite ↑↑ |
| B2 | **Submit Devpost** — salin `DEVPOST_DRAFT.md` + 5 screenshot + URL | [ ] | Progress ↑↑ |
| B3 | **README** selaras (Sentry, `.venv`, tanpa klaim 85% palsu) | [x] |
| B4 | Perluas eval / tuning ambang (opsional) | [ ] | Feasibility ↑ |
| B5 | Metrik AI vs manusia dari DB (butuh persist `/scan` atau manual) | [ ] | Opsional |
| B6 | Video demo | [ ] | Anda tunda — lakukan terakhir |

**Jangan** centang challenge Hud.io di Devpost tanpa integrasi SDK.

---

## Fokus berikutnya (detail)

- [~] **Buildkite end-to-end** — smoke + webhook backend: [`docs/BUKTI_BUILDKITE.md`](docs/BUKTI_BUILDKITE.md); UI + API token: Anda
- [x] **Dataset eval mini** — [`scripts/eval_deteksi.py`](../scripts/eval_deteksi.py), [`docs/HASIL_EVAL_DETEKSI.md`](docs/HASIL_EVAL_DETEKSI.md) (bukan klaim 85%+)
- [ ] **Metrik AI vs manusia** — backlog (persist scan atau agregat manual)
- [x] **Draf Devpost** — [`docs/DEVPOST_DRAFT.md`](docs/DEVPOST_DRAFT.md); screenshot + submit oleh Anda

---

## Selesai — Day 5–6 + infrastruktur

- [x] Sentry, `make qa`, hook/rule QA Cursor
- [x] Frontend SPA + deploy (`guardrail` + `guardrail-api` subdomain)
- [x] CORS, Buildkite kode + docs pipeline

---

## Week 1 ringkas

| Day | Status |
|-----|--------|
| 1–3 | ✅ Backend + deteksi + analisis |
| 4 | ✅ Kode Buildkite; [ ] bukti pipeline Anda |
| 5 | ✅ Sentry + deploy |
| 6 | ✅ Dashboard |
| 7 | [x] QA + dok; [ ] E2E opsional |

## Week 2

- [ ] Video (Anda)
- [ ] Devpost submit final
- [ ] Buffer sebelum **28 Mei 2026 01:00 WIB**

---

## Success metrics (jujur)

| Item | Status |
|------|--------|
| API + dashboard live | ✅ |
| 20+ aturan risiko | ✅ |
| Integrasi sponsor **terbukti** | 🔄 Buildkite menunggu token + screenshot Anda |
| Eval terukur (mini) | ✅ lihat HASIL_EVAL |
| Devpost lengkap | 🔄 draf siap |
| Video | ⏸️ |

---

**Next action untuk Anda:** B1 (Buildkite token + 1 build) → B2 (Devpost + screenshot) → B6 (video).
