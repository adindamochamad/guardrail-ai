# Draf Devpost — salin ke formulir submission

> Sesuaikan nama tim & tautan sebelum submit. Video: tambahkan URL setelah rekaman.

---

## Project name

**GuardRail AI**

---

## Elevator pitch

Developers ship AI-generated code every day, but generic linters miss AI-specific risks. GuardRail AI detects likely AI-authored code, applies tailored security rules, and blocks critical findings in CI—live at **https://guardrail.adindamochamad.com** with API **https://guardrail-api.adindamochamad.com**.

---

## The Whole Story

### Inspiration

Studies and team anecdotes point to a growing share of production code written with Copilot, Cursor, and similar tools—often merged with less review than human-written changes. Classic SAST tools were not designed for “code that might be AI-shaped” or for commit metadata like Copilot co-author trailers.

### What it does

- **Detect** whether a snippet is likely AI-generated (patterns, optional Git commit signals, optional LLM).
- **Analyze** with 30+ regex rules and Python AST checks, including rules that apply primarily when code is treated as AI-generated.
- **Scan** end-to-end via `POST /scan` (used by our React dashboard).
- **Integrate with Buildkite**: webhook annotations plus a pipeline step that fails the build on CRITICAL findings (`scripts/guardrail_ci_scan.sh`).
- **Observe production** with Sentry (runtime errors); Hud.io integration is on our roadmap.

### How we built it

- **Backend:** FastAPI 0.6, SQLAlchemy, SQLite, pytest (39 tests), ruff.
- **Frontend:** React, TypeScript, Vite, Tailwind—calls the public API with CORS.
- **Deploy:** VPS + nginx; API on `guardrail-api.*`, dashboard on `guardrail.*`.
- **Quality:** `make qa` runs lint, tests, and production frontend build.

### Challenges we overcame

- Port conflicts and multi-tenant VPS layout (API on 8008 behind nginx).
- CORS for a separate dashboard origin.
- Separating **webhook annotations** from **hard CI fail**—documented both paths clearly.
- Honest observability: Sentry in production while Hud.io remains waitlisted.

### Achievements we're proud of

- **Live demo:** dashboard scan with severity breakdown and findings table.
- **Automated tests:** 39 pytest cases; reproducible eval script on a labeled mini-set ([`docs/HASIL_EVAL_DETEKSI.md`](HASIL_EVAL_DETEKSI.md)).
- **CI-ready:** Buildkite pipeline example + shell scanner against `/scan`.
- **Open API:** Swagger at `/docs` for judges to try payloads.

### What we learned

Heuristic detection needs labeled evaluation before marketing accuracy claims. Combining detection + analysis in one `/scan` keeps UX and CI consistent. Sponsor integrations must be **demonstrated**, not only described.

### What's next

- Expand labeled evaluation set; optional LLM mode in CI.
- Persist scan history for AI vs human trend metrics.
- Hud.io runtime SDK when access is available.
- SaaS pricing experiment: freemium API tier for small teams.

### Impact

Fewer critical issues (e.g. `eval`, hardcoded secrets) reaching main branches when teams adopt GuardRail as a pre-merge gate for AI-assisted development.

---

## Built with

`python`, `fastapi`, `sqlalchemy`, `react`, `typescript`, `vite`, `tailwindcss`, `buildkite`, `sentry`, `openai`, `pytest`, `ruff`, `nginx`

*(Do not list `hud-sdk` unless integrated.)*

---

## Try it out

- Dashboard: https://guardrail.adindamochamad.com  
- API docs: https://guardrail-api.adindamochamad.com/docs  
- Repo: https://github.com/adindamochamad/guardrail-ai  

---

## Sponsor challenges (recommended)

- [x] **Buildkite** — primary; show pipeline step + optional webhook  
- [ ] Hud.io — only if SDK integrated  
- [ ] Jellyfish — optional future metrics  

---

## Image gallery (capture these)

1. Dashboard — empty state / form  
2. Dashboard — after scan (detection card + severity chart)  
3. Findings table with **CRITICAL** row  
4. Swagger `/docs` on API host  
5. Buildkite step failed (red) or annotation screenshot  

---

## Video demo (structure — record later)

1. Problem (15s)  
2. Live dashboard scan with risky Python snippet (60s)  
3. Buildkite block or annotation (30s)  
4. Feasibility / CTA (15s)  
