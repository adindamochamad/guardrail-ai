# GuardRail AI - TODO Checklist

## 🎯 Hari ini — Day 5 (21 Mei 2026)

### 🔄 Fokus berikutnya (Day 5)
- [ ] Metrik perbandingan AI vs manusia & demo deployment (opsional; Hud.io waitlist — pakai Sentry + dashboard sendiri)

### ✅ Selesai — Day 5 (parsial)
- [x] Observabilitas runtime lewat **Sentry** (`src/observabilitas/`), env & `GET /health` + docs [`OBSERVABILITAS_RUNTIME.md`](docs/OBSERVABILITAS_RUNTIME.md); app **v0.5.0**

### ✅ Selesai — Day 4 (20 Mei 2026)
- [x] Webhook `POST /webhooks/buildkite` — verifikasi token / HMAC, pemindaian, anotasi API opsional
- [x] Modul `src/integrasi_buildkite/` — klien anotasi, orkestrator, opsi git clone ringkas
- [x] Konfigurasi env Buildkite; tes + `docs/API.md`; app **v0.4.0** (kini **v0.5.0** dengan Sentry)
- [x] Dokumentasi ambang blokir CRITICAL di pipeline Buildkite (langkah `guardrail` dengan exit non-zero)

### ✅ Selesai — Day 3 (19 Mei 2026)
- [x] Paket `src/analisis_risiko/` — **≥30 aturan regex** + **11 pemeriksaan AST** Python
- [x] `POST /analyze` dan `POST /scan` (deteksi → analisis konsisten)
- [x] Tes unit + HTTP; `docs/API.md` diperbarui; app `v0.3.0`

### ✅ Riwayat Day 2 (18 Mei 2026)
- [x] Modul `src/ai_detector/`, `POST /detect`, OpenAI opsional, dsb.

---

## ✅ Riwayat Day 1 (17 Mei 2026)

### Completed
- [x] Create project folder structure
- [x] Write competition documentation (COMPETITION.md)
- [x] Write project technical documentation (PROJECT.md)
- [x] Write 11-day development roadmap (ROADMAP.md)
- [x] Create README.md
- [x] Create .gitignore
- [x] Cursor rules (`.cursor/rules/*.mdc`) — konteks proyek setiap prompt
- [x] Initialize Git repository
- [x] Backend FastAPI (`backend/`) — `/health`, `/db/ping`, ORM Day 1
- [x] Skema database SQLite — `scans`, `code_files`, `ai_detections`, `risks`
- [x] Makefile, ruff, pytest, `.pre-commit-config.yaml` (opsional)
- [x] Dokumentasi API awal (`docs/API.md`), panduan backend (`backend/README.md`)

---

## 📋 Week 1: Core Development (Days 2-7)

### Day 2 - AI Detection Engine
- [x] AI detection module (`src/ai_detector/`)
- [x] Pattern database (20+ rules in `pola_kode.py`)
- [x] OpenAI integration (opsional, `layanan_llm.py`)
- [ ] Dataset/uji akurasi terukur vs target 85%+ (evaluasi manual / set berlabel)

### Day 3 - Risk Analysis Engine
- [x] Risk rules database (30+ regex + 11 AST Python)
- [x] Security / logic / performance / compliance rules (baseline)
- [x] Risk analysis engine (`analisis_risiko.mesin`)
- [x] API endpoints: `/analyze`, `/scan`

### Day 4 - Buildkite Integration
- [x] Buildkite REST: anotasi build (`kirim_anotasi_build`)
- [x] Webhook handler (`/webhooks/buildkite`)
- [x] Code fetching (git clone ringkas opsional, `BUILDKITE_WEBHOOK_GIT_CLONE`)
- [x] Blokir build terpusat lewat langkah pipeline + dokumentasi (bukan hanya anotasi)

### Day 5 - Runtime observability (Hud.io waitlist → Sentry)
- [x] SDK observabilitas: Sentry + fasad `observabilitas/`
- [x] Koleksi error (dan trace opsional) lewat `SENTRY_*`
- [ ] Perbandingan AI vs manusia terukur (butuh produk / dataset — lanjut jika ada waktu)
- [ ] Deploy demo publik (Railway, Fly.io, dsb.)

### Day 6 - Dashboard Frontend
- [ ] React app setup
- [ ] Overview dashboard
- [ ] Scan results page
- [ ] Metrics visualization

### Day 7 - Testing & Polish
- [ ] End-to-end testing
- [ ] Bug fixes
- [ ] Performance optimization
- [ ] Documentation updates

---

## 📹 Week 2: Demo & Submission (Days 8-11)

### Day 8 - Demo Video
- [ ] Write demo script
- [ ] Record demo (3 scenarios)
- [ ] Video editing
- [ ] Upload to YouTube

### Day 9 - Submission Materials
- [ ] Capture screenshots (5 images)
- [ ] Write Devpost submission
- [ ] Create project on Devpost
- [ ] Select sponsor challenges

### Day 10 - Final Submission
- [ ] Final review
- [ ] Submit to Devpost
- [ ] Verify submission confirmed
- [ ] Backup all materials

### Day 11 - Buffer
- [ ] Handle any issues
- [ ] Final improvements
- [ ] Prepare for judging

---

## 🎯 Critical Deadlines

- **Deadline**: 28 Mei 2026, 01:00 WIB (10:00 AM PDT)
- **Judging**: 28 Mei, 01:00 - 04:00 WIB
- **Winners**: 28 Mei, 06:30 WIB

**Days Remaining**: 11 days

---

## 🏆 Success Metrics

### Minimum Viable (75% probability)
- [ ] AI detection working (85%+ accuracy)
- [ ] 20+ risk rules
- [ ] 1 integration (Buildkite OR Hud.io)
- [ ] Basic dashboard
- [ ] Demo video
- [ ] Devpost submission complete

### Target (60% probability)
- [ ] Everything above +
- [ ] Both Buildkite AND Hud.io working
- [ ] 30+ risk rules
- [ ] Professional dashboard
- [ ] High-quality demo

### Stretch (45% probability)
- [ ] Everything above +
- [ ] Jellyfish integration
- [ ] 50+ risk rules
- [ ] Killer demo video
- [ ] Comprehensive docs

---

## 💰 Prize Targets

### Sponsor Challenges
- [ ] Hud.io Challenge (90% win probability) - $500-1,000
- [ ] Buildkite Challenge (80% win probability) - $500-1,000
- [ ] Jellyfish Challenge (60% win probability) - $500
- [ ] TrueFoundry Challenge (40% stretch) - $1,000-1,500

### Overall Winner
- [ ] Overall Winner (45% probability) - $2,000 value + exposure

**Expected Total Winnings**: $2,800

---

## 🚨 Quick Reference

### Project Structure
```
guardrail-ai/
├── .cursor/rules/         ✅ Aturan Cursor (alwaysApply)
├── backend/               ✅ FastAPI Day 3 (deteksi + analisis)
│   ├── src/
│   │   ├── ai_detector/
│   │   ├── analisis_risiko/
│   │   └── routes/
│   ├── tests/
│   └── README.md
├── docs/
│   ├── COMPETITION.md    ✅ Complete
│   ├── PROJECT.md        ✅ Complete
│   ├── ROADMAP.md        ✅ Complete
│   └── API.md            ✅ Day 2 (detect)
├── frontend/             ⏳ To build
├── README.md             ✅ Complete
├── Makefile              ✅ Perintah dev
├── TODO.md               ✅ This file
└── .gitignore            ✅ Complete
```

### Documentation Links
- [Competition Details](docs/COMPETITION.md)
- [Technical Docs](docs/PROJECT.md)
- [Development Roadmap](docs/ROADMAP.md)
- [API (Day 3)](docs/API.md)

### Resources
- Devpost: https://devnetwork-ai-ml-hack-2026.devpost.com
- Hud.io Docs: https://docs.hud.io
- Buildkite Docs: https://buildkite.com/docs

---

## 💪 Daily Progress Tracking

### Day 1 (17 Mei) — ✅ Backend foundation & rules
### Day 2 (18 Mei) — ✅ Deteksi AI + `/detect`
### Day 3 (19 Mei) — ✅ Analisis risiko + `/analyze` + `/scan`
### Day 4 (20 Mei) - 🔄 Pending
### Day 5 (21 Mei) - 🔄 Pending
### Day 6 (22 Mei) - 🔄 Pending
### Day 7 (23 Mei) - 🔄 Pending
### Day 8 (24 Mei) - 🔄 Pending
### Day 9 (25 Mei) - 🔄 Pending
### Day 10 (26 Mei) - 🔄 Pending
### Day 11 (27 Mei) - 🔄 Pending

---

**Status**: Day 3 selesai — ≥30 aturan regex, AST Python, `/analyze`, `/scan`  
**Next**: Day 4 — integrasi Buildkite
**Time Remaining**: 11 days
