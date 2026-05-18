# GuardRail AI - Development Roadmap (11 Days)

## 📅 Timeline Overview

**Start Date**: 17 Mei 2026 (Hari ini, 17:30 WIB)
**Deadline**: 28 Mei 2026, 01:00 WIB (29 Mei dini hari)
**Total Days**: 11 hari development time

**Strategy**: 
- Days 1-7: Core development (intensive coding)
- Days 8-9: Polish, testing, demo preparation
- Days 10-11: Submission & buffer

---

## 🎯 Daily Breakdown

### **DAY 1 - Setup & Foundation** (17 Mei 2026 - TODAY)
**Goal**: Project setup, architecture decisions, basic scaffolding

#### Morning (3 hours)
- [x] ✅ Create project folder structure
- [x] ✅ Write competition documentation
- [x] ✅ Write project technical documentation
- [x] ✅ Write roadmap (this document)
- [ ] Setup Git repository
- [ ] Create .gitignore (Python, Node, env files)
- [ ] Initialize README.md with project overview

#### Afternoon (4 hours)
- [ ] **Backend setup**
  - [ ] Create FastAPI app structure
  - [ ] Setup virtual environment (venv)
  - [ ] Install dependencies: fastapi, uvicorn, pydantic
  - [ ] Create basic health check endpoint (`/health`)
  - [ ] Test server runs successfully

- [ ] **Database setup**
  - [ ] Create SQLite database schema
  - [ ] Tables: scans, risks, code_files, ai_detections
  - [ ] Setup SQLAlchemy models
  - [ ] Create migration script

- [ ] **Development tools**
  - [ ] Setup pytest for testing
  - [ ] Configure ruff for linting
  - [ ] Create Makefile for common commands
  - [ ] Setup pre-commit hooks

#### Evening (2 hours)
- [ ] **Research & planning**
  - [ ] Read Hud.io SDK documentation
  - [ ] Read Buildkite API documentation
  - [ ] Test Hud.io installation: `pip install hud-sdk`
  - [ ] Get Buildkite API token (if available)
  - [ ] Sketch out API endpoint structure

- [ ] **Documentation**
  - [ ] Create API documentation template
  - [ ] Document database schema
  - [ ] List all endpoints to implement

**Deliverables Day 1:**
- ✅ Complete project structure
- ✅ FastAPI server running
- ✅ Database initialized
- ✅ Development environment ready

**Time commitment**: 9 hours

---

### **DAY 2 - AI Code Detection Engine** (18 Mei 2026)
**Goal**: Build core AI detection functionality

#### Morning (4 hours)
- [ ] **AI Detection Module**
  - [ ] Create `src/ai_detector/` module
  - [ ] Implement `detect_ai_code()` function
  - [ ] Pattern-based detection (regex rules)
  - [ ] Git metadata parser (check for Copilot markers)
  - [ ] Confidence score calculation

- [ ] **Pattern Database**
  - [ ] Define 20+ AI code patterns (variable names, comments, structure)
  - [ ] Create pattern matching engine
  - [ ] Test patterns on sample code
  - [ ] Measure accuracy on test dataset

#### Afternoon (4 hours)
- [ ] **OpenAI Integration**
  - [ ] Setup OpenAI API client
  - [ ] Implement LLM-based classification
  - [ ] Create prompt template for code analysis
  - [ ] Test on 10 sample files (5 AI, 5 human)
  - [ ] Optimize prompt for accuracy vs cost

- [ ] **Hybrid Detection**
  - [ ] Combine pattern matching + LLM classification
  - [ ] Weighted scoring algorithm
  - [ ] Fallback logic (if LLM unavailable)
  - [ ] Performance optimization (cache results)

#### Evening (2 hours)
- [ ] **Testing & Validation**
  - [ ] Create test dataset (20 files: 10 AI, 10 human)
  - [ ] Run detection on test set
  - [ ] Calculate precision, recall, F1 score
  - [ ] Target: 85%+ precision, 90%+ recall
  - [ ] Fix issues if below target

**Deliverables Day 2:**
- ✅ AI detection engine working
- ✅ Accuracy: 85%+ on test set
- ✅ API endpoint: `POST /detect` (input: code, output: is_ai + confidence)

**Time commitment**: 10 hours

---

### **DAY 3 - Risk Analysis Engine** (19 Mei 2026)
**Goal**: Build vulnerability detection system

#### Morning (4 hours)
- [ ] **Risk Rules Database**
  - [ ] Create `src/risk_analyzer/` module
  - [ ] Define 30+ risk rules (JSON/YAML format)
  - [ ] Categories: Security, Logic, Performance, Compliance
  - [ ] For each rule: pattern, severity, description, fix suggestion

- [ ] **Security Rules (Priority)**
  - [ ] SQL injection detection
  - [ ] Hardcoded secrets (API keys, passwords)
  - [ ] Command injection (os.system, subprocess)
  - [ ] Path traversal vulnerabilities
  - [ ] XSS patterns

#### Afternoon (4 hours)
- [ ] **Risk Analysis Engine**
  - [ ] Implement `analyze_code()` function
  - [ ] Pattern matching against rules
  - [ ] AST parsing for semantic analysis
  - [ ] Severity scoring algorithm
  - [ ] Line number extraction (for error highlighting)

- [ ] **AI-Specific Rules**
  - [ ] Increase sensitivity for AI-detected code
  - [ ] AI-specific patterns (common AI mistakes)
  - [ ] Weighted scoring (AI code = higher risk weight)

#### Evening (2 hours)
- [ ] **Testing & Refinement**
  - [ ] Create vulnerable code samples (10 files)
  - [ ] Run risk analysis
  - [ ] Verify all vulnerabilities detected
  - [ ] Reduce false positives (tune thresholds)
  - [ ] API endpoint: `POST /analyze` (input: code + is_ai, output: risks[])

**Deliverables Day 3:**
- ✅ Risk analysis engine working
- ✅ 30+ risk rules implemented
- ✅ False positive rate < 15%
- ✅ API endpoints: `/detect` + `/analyze` + `/scan` (combined)

**Time commitment**: 10 hours

---

### **DAY 4 - Buildkite Integration** (20 Mei 2026)
**Goal**: CI/CD integration with Buildkite

#### Morning (3 hours)
- [ ] **Buildkite API Client**
  - [ ] Create `src/integrations/buildkite/` module
  - [ ] Implement Buildkite API wrapper
  - [ ] Test API connection (list pipelines)
  - [ ] Test webhook creation

- [ ] **Webhook Handler**
  - [ ] Create FastAPI webhook endpoint: `POST /webhooks/buildkite`
  - [ ] Parse webhook payload (build.started, build.finished)
  - [ ] Extract repo URL, commit hash, branch
  - [ ] Verify webhook signature (security)

#### Afternoon (4 hours)
- [ ] **Code Fetching**
  - [ ] Implement Git clone functionality
  - [ ] Clone repo at specific commit
  - [ ] Extract changed files (diff from base branch)
  - [ ] Filter relevant files (exclude node_modules, etc.)

- [ ] **Scan Orchestration**
  - [ ] On webhook trigger: fetch code → scan files → post results
  - [ ] Parallel scanning (multiple files at once)
  - [ ] Progress tracking
  - [ ] Error handling (repo clone fails, etc.)

#### Evening (3 hours)
- [ ] **Results Posting**
  - [ ] Format scan results as Buildkite annotation (Markdown)
  - [ ] Post annotation via API
  - [ ] Set build status (pass/fail based on risks)
  - [ ] Block build if CRITICAL risks found
  - [ ] Create PR comment with detailed results

- [ ] **Testing**
  - [ ] Setup test Buildkite pipeline
  - [ ] Trigger build → verify webhook received
  - [ ] Verify scan runs and results posted
  - [ ] Verify build blocked on critical risk

**Deliverables Day 4:**
- ✅ Buildkite integration working end-to-end
- ✅ Webhook handler functional
- ✅ Build blocking on critical risks
- ✅ Results posted as annotations

**Time commitment**: 10 hours

---

### **DAY 5 - Hud.io Integration** (21 Mei 2026)
**Goal**: Runtime monitoring integration

#### Morning (3 hours)
- [ ] **Hud.io SDK Setup**
  - [ ] Install hud-sdk: `pip install hud-sdk`
  - [ ] Create demo app with Hud.io instrumentation
  - [ ] Test: function with `@hud.track()` decorator
  - [ ] Verify data appears in Hud.io dashboard

- [ ] **Hud.io API Client**
  - [ ] Read Hud.io API documentation
  - [ ] Create API wrapper: `src/integrations/hud/`
  - [ ] Test: fetch metrics for instrumented function
  - [ ] Parse metrics: invocations, duration, errors

#### Afternoon (4 hours)
- [ ] **Metrics Collection**
  - [ ] Implement `fetch_function_metrics(function_name, timeframe)`
  - [ ] Aggregate metrics across multiple functions
  - [ ] Calculate: error rate, avg latency, exception types
  - [ ] Store metrics in database (time-series data)

- [ ] **AI vs Human Comparison**
  - [ ] Tag functions in DB (ai_generated: true/false)
  - [ ] Fetch metrics for AI functions
  - [ ] Fetch metrics for human functions
  - [ ] Calculate comparison ratios
  - [ ] API endpoint: `GET /metrics/comparison`

#### Evening (3 hours)
- [ ] **Dashboard Data**
  - [ ] Create metrics summary endpoint
  - [ ] Recent incidents (errors from Hud.io)
  - [ ] Top failing functions
  - [ ] Performance trends (7 days)
  - [ ] Correlate Hud.io errors with GuardRail scan results

- [ ] **Testing**
  - [ ] Deploy demo app with AI-generated buggy code
  - [ ] Trigger errors in production
  - [ ] Verify Hud.io captures errors
  - [ ] Verify GuardRail correlates errors to AI code

**Deliverables Day 5:**
- ✅ Hud.io integration working
- ✅ Metrics fetching functional
- ✅ AI vs Human comparison API ready
- ✅ Demo app with instrumentation deployed

**Time commitment**: 10 hours

---

### **DAY 6 - Dashboard Frontend** (22 Mei 2026)
**Goal**: Build web UI for visualization

#### Morning (3 hours)
- [ ] **Frontend Setup**
  - [ ] Create React app with Vite
  - [ ] Setup TailwindCSS
  - [ ] Install Recharts (for graphs)
  - [ ] Create routing (React Router)
  - [ ] Basic layout (header, sidebar, content)

- [ ] **Pages Structure**
  - [ ] `/` - Overview dashboard
  - [ ] `/scans` - Scan results list
  - [ ] `/risks` - Risk details
  - [ ] `/metrics` - Hud.io metrics (AI vs human)
  - [ ] `/settings` - Configuration

#### Afternoon (4 hours)
- [ ] **Overview Dashboard**
  - [ ] Stats cards (total scans, risks found, AI code %)
  - [ ] Risk distribution chart (pie chart: critical, high, medium, low)
  - [ ] Recent scans table
  - [ ] AI vs Human metrics comparison (bar chart)

- [ ] **Scan Results Page**
  - [ ] List all scans (table with filters)
  - [ ] Click scan → detailed view
  - [ ] Code viewer with risk highlighting
  - [ ] Line-by-line annotations
  - [ ] Fix suggestions display

#### Evening (3 hours)
- [ ] **Metrics Page**
  - [ ] Hud.io metrics visualization
  - [ ] Time-series charts (error rate over time)
  - [ ] Comparison: AI code vs Human code
  - [ ] Top failing functions list
  - [ ] Drill-down to function details

- [ ] **Polish**
  - [ ] Responsive design (mobile-friendly)
  - [ ] Loading states
  - [ ] Error handling
  - [ ] Empty states ("No scans yet")

**Deliverables Day 6:**
- ✅ Dashboard UI working
- ✅ All pages functional
- ✅ Connected to backend APIs
- ✅ Professional, clean design

**Time commitment**: 10 hours

---

### **DAY 7 - Integration Testing & Polish** (23 Mei 2026)
**Goal**: End-to-end testing, bug fixes, polish

#### Morning (3 hours)
- [ ] **End-to-End Testing**
  - [ ] Test full flow: Push code → Buildkite webhook → Scan → Results posted
  - [ ] Test AI detection accuracy on real codebases
  - [ ] Test risk detection on vulnerable code samples
  - [ ] Test Hud.io metrics fetching
  - [ ] Test dashboard displays correct data

- [ ] **Bug Fixes**
  - [ ] Fix any broken flows
  - [ ] Handle edge cases (empty files, binary files, etc.)
  - [ ] Improve error messages
  - [ ] Add validation (input sanitization)

#### Afternoon (4 hours)
- [ ] **Performance Optimization**
  - [ ] Optimize scan speed (parallel processing)
  - [ ] Cache AI detection results (avoid duplicate LLM calls)
  - [ ] Database indexing (speed up queries)
  - [ ] Frontend code splitting (faster load)
  - [ ] Compress assets

- [ ] **Documentation**
  - [ ] Update README.md with setup instructions
  - [ ] API documentation (OpenAPI/Swagger)
  - [ ] User guide (how to use GuardRail)
  - [ ] Architecture diagram (create visual)
  - [ ] Code comments (clean up)

#### Evening (3 hours)
- [ ] **Demo Preparation**
  - [ ] Prepare demo scenarios (3 scenarios for video)
  - [ ] Create sample vulnerable code
  - [ ] Setup demo repository with AI code
  - [ ] Test demo flow multiple times
  - [ ] Note any issues to fix tomorrow

- [ ] **Polish**
  - [ ] UI/UX improvements (spacing, colors, fonts)
  - [ ] Logo design (if time permits)
  - [ ] Error messages user-friendly
  - [ ] Loading spinners, progress indicators

**Deliverables Day 7:**
- ✅ All features working end-to-end
- ✅ Major bugs fixed
- ✅ Documentation complete
- ✅ Demo scenarios ready

**Time commitment**: 10 hours

---

## 📹 Days 8-9: Demo & Submission Prep

### **DAY 8 - Demo Video Creation** (24 Mei 2026)
**Goal**: Record professional demo video

#### Morning (3 hours)
- [ ] **Demo Script Writing**
  - [ ] Write full script (word-by-word)
  - [ ] Time each section (ensure < 3 minutes total)
  - [ ] Practice delivery (natural, not robotic)
  - [ ] Prepare screen flows (what to show when)

- [ ] **Demo Setup**
  - [ ] Clean up desktop (remove distractions)
  - [ ] Prepare demo repository
  - [ ] Setup screen recording software (OBS/Loom)
  - [ ] Test microphone quality
  - [ ] Test screen resolution (1080p)

#### Afternoon (4 hours)
- [ ] **Recording**
  - [ ] Record intro (problem statement)
  - [ ] Record demo (3 scenarios):
    1. AI code with SQL injection detected
    2. Buildkite integration blocking build
    3. Hud.io metrics showing AI code issues
  - [ ] Record business pitch (market, pricing)
  - [ ] Record outro (call to action)

- [ ] **Re-takes**
  - [ ] Review recordings
  - [ ] Re-record sections that need improvement
  - [ ] Ensure clear audio, smooth demo

#### Evening (3 hours)
- [ ] **Video Editing**
  - [ ] Import clips to editor (DaVinci Resolve/iMovie)
  - [ ] Cut out mistakes, awkward pauses
  - [ ] Add transitions (subtle, professional)
  - [ ] Add text overlays (highlight key points)
  - [ ] Background music (optional, subtle)
  - [ ] Export as MP4 (1080p)

- [ ] **Upload & Test**
  - [ ] Upload to YouTube (unlisted)
  - [ ] Test video plays correctly
  - [ ] Add captions (if time permits)
  - [ ] Get shareable link

**Deliverables Day 8:**
- ✅ Demo video complete (2-3 minutes)
- ✅ Uploaded to YouTube
- ✅ Professional quality (clear audio, smooth demo)

**Time commitment**: 10 hours

---

### **DAY 9 - Screenshots & Devpost Writing** (25 Mei 2026)
**Goal**: Create all submission materials

#### Morning (3 hours)
- [ ] **Screenshots**
  - [ ] Dashboard overview (annotate key features)
  - [ ] Code analysis view (show risk highlighting)
  - [ ] Buildkite integration (show pipeline)
  - [ ] Hud.io metrics comparison (AI vs human chart)
  - [ ] Architecture diagram (draw in Excalidraw/Figma)

- [ ] **Image Editing**
  - [ ] Crop to 1280x720
  - [ ] Add annotations (arrows, callouts)
  - [ ] Ensure readable (high contrast, clear text)
  - [ ] Export as PNG

#### Afternoon (5 hours)
- [ ] **Devpost Writing**
  - [ ] Write "Inspiration" section
  - [ ] Write "What It Does" (feature list)
  - [ ] Write "How We Built It" (tech stack)
  - [ ] Write "Challenges We Overcame"
  - [ ] Write "Accomplishments" (metrics, achievements)
  - [ ] Write "What We Learned"
  - [ ] Write "What's Next" (business model, roadmap)
  - [ ] Write sponsor integrations section (Hud.io, Buildkite, Jellyfish)

- [ ] **Elevator Pitch**
  - [ ] Draft 3 versions
  - [ ] Get feedback (from friend or ChatGPT)
  - [ ] Pick best version
  - [ ] Ensure < 2 sentences

#### Evening (2 hours)
- [ ] **Devpost Project Creation**
  - [ ] Create project on Devpost
  - [ ] Fill all required fields
  - [ ] Upload screenshots (5 images)
  - [ ] Add demo video link
  - [ ] Add GitHub repo link
  - [ ] Add "Built With" tags
  - [ ] Select sponsor challenges (Hud.io, Buildkite, Jellyfish)

- [ ] **Review**
  - [ ] Proofread everything (typos, grammar)
  - [ ] Test all links work
  - [ ] Ensure video plays
  - [ ] Ensure images display correctly

**Deliverables Day 9:**
- ✅ 5 professional screenshots
- ✅ Complete Devpost submission (draft)
- ✅ All materials ready for submission

**Time commitment**: 10 hours

---

## 🚀 Days 10-11: Final Submission & Buffer

### **DAY 10 - Final Review & Submission** (26 Mei 2026)
**Goal**: Submit project, ensure everything perfect

#### Morning (3 hours)
- [ ] **Final Testing**
  - [ ] Test all features one last time
  - [ ] Test on fresh browser (clear cache)
  - [ ] Test demo video on different devices
  - [ ] Verify GitHub repo is public
  - [ ] Verify all links work

- [ ] **Devpost Final Review**
  - [ ] Read entire submission aloud
  - [ ] Check for typos, grammar errors
  - [ ] Ensure coherent narrative
  - [ ] Verify metrics cited are accurate
  - [ ] Verify sponsor integrations highlighted

#### Afternoon (2 hours)
- [ ] **Competitive Analysis**
  - [ ] Check other submissions (if visible)
  - [ ] Identify gaps in our submission
  - [ ] Add any missing elements
  - [ ] Strengthen weak sections

- [ ] **Enhancement**
  - [ ] Add any last-minute polish
  - [ ] Improve screenshots (if needed)
  - [ ] Sharpen elevator pitch
  - [ ] Add missing "Built With" tags

#### Evening (2 hours)
- [ ] **SUBMIT TO DEVPOST**
  - [ ] Click "Submit to Hackathon"
  - [ ] Verify submission went through
  - [ ] Take screenshot of submission confirmation
  - [ ] Save confirmation email

- [ ] **Backup**
  - [ ] Export Devpost submission as PDF
  - [ ] Backup video file locally
  - [ ] Backup all screenshots
  - [ ] Push final code to GitHub

**Deliverables Day 10:**
- ✅ PROJECT SUBMITTED TO DEVPOST
- ✅ Confirmation received
- ✅ 2 days before deadline (safe buffer)

**Time commitment**: 7 hours

---

### **DAY 11 - Buffer & Improvements** (27 Mei 2026)
**Goal**: Handle unexpected issues, improvements

#### All Day (flexible)
- [ ] **If issues found:**
  - [ ] Fix any last-minute bugs
  - [ ] Re-record demo video if needed
  - [ ] Update Devpost submission (allowed until deadline)
  - [ ] Improve weak areas

- [ ] **If no issues:**
  - [ ] Add bonus features (if energy left)
  - [ ] Create blog post about project
  - [ ] Tweet about submission
  - [ ] Prepare for potential interview (if selected)

- [ ] **Final check:**
  - [ ] Ensure submission visible on Devpost
  - [ ] Ensure selected all sponsor challenges
  - [ ] Ensure demo video accessible
  - [ ] Relax, project is done!

**Deliverables Day 11:**
- ✅ Buffer day for unexpected issues
- ✅ All improvements implemented
- ✅ Ready for judging on Day 12

**Time commitment**: 0-5 hours (as needed)

---

## ⏰ Deadline Day (28 Mei 2026)

### **Final Hours (00:00 - 01:00 WIB)**
- [ ] **00:00 WIB**: Wake up, final final check
- [ ] **00:30 WIB**: Verify submission still visible
- [ ] **00:45 WIB**: Last chance for edits (if needed)
- [ ] **01:00 WIB**: DEADLINE (10:00 AM PDT)

### **After Submission (01:00 - 18:00 WIB)**
- Wait for judging results
- Judging period: 10:00 AM - 1:00 PM PT (01:00 - 04:00 WIB Rabu malam/Kamis pagi)
- Winners announced: 3:30 PM PT (06:30 WIB Kamis pagi)

---

## 📊 Time Commitment Summary

| Phase | Days | Hours/Day | Total Hours |
|-------|------|-----------|-------------|
| Core Development | Days 1-7 | 10h | 70h |
| Demo & Submission | Days 8-9 | 10h | 20h |
| Final Review | Day 10 | 7h | 7h |
| Buffer | Day 11 | 0-5h | 2.5h |
| **TOTAL** | **11 days** | **9h avg** | **~100h** |

**Realistic workload**: ~9 hours/day average
**Intensity**: High (especially Days 1-7)
**Feasibility**: Achievable for solo developer with focus

---

## 🎯 Daily Checkpoints

### Each Evening: Review Progress
- [ ] What did I accomplish today?
- [ ] Am I on track with roadmap?
- [ ] Any blockers for tomorrow?
- [ ] Any adjustments needed to plan?

### Red Flags (Adjust if any occur):
- ⚠️ Behind schedule by > 1 day → cut features, focus on MVP
- ⚠️ Major blocker (API not working) → pivot approach
- ⚠️ Scope too large → simplify, reduce features
- ⚠️ Quality suffering → slow down, prioritize polish

---

## 🚨 Contingency Plans

### If Behind Schedule:

**Priority 1 (Must have for submission):**
- AI detection engine
- Risk analysis (20+ rules minimum)
- Buildkite OR Hud.io integration (at least one)
- Basic dashboard
- Demo video

**Priority 2 (Nice to have):**
- Both Buildkite AND Hud.io integrations
- Jellyfish integration
- Advanced dashboard features

**Priority 3 (Can skip):**
- CLI tool
- GitHub Actions support
- Email notifications

### If Ahead of Schedule:

**Bonus features:**
- GitHub Actions integration (in addition to Buildkite)
- Jellyfish integration (engineering metrics)
- VS Code extension (basic)
- More comprehensive risk rules (50+ instead of 30+)
- Better UI/UX polish

---

## ✅ Success Criteria (Reminder)

### Minimum Viable Submission:
- [x] Working AI detection (85%+ accuracy)
- [ ] 20+ risk rules implemented
- [ ] 1 integration working (Buildkite or Hud.io)
- [ ] Basic dashboard
- [ ] 2-3 minute demo video
- [ ] Complete Devpost submission

### Target Submission:
- [ ] Everything above +
- [ ] Both Buildkite AND Hud.io working
- [ ] 30+ risk rules
- [ ] Professional dashboard
- [ ] High-quality demo video
- [ ] Strong business narrative

### Stretch Submission:
- [ ] Everything above +
- [ ] Jellyfish integration
- [ ] 50+ risk rules
- [ ] Advanced dashboard features
- [ ] Killer demo video (production quality)
- [ ] Comprehensive documentation

---

## 💪 Motivation & Mindset

### Daily Mantra:
"11 days to build something judges will remember. Focus on impact, not perfection."

### When Stuck:
1. Take 10-minute break
2. Explain problem to rubber duck
3. Search documentation
4. Ask AI assistant (ChatGPT, Claude)
5. Simplify the problem
6. Move to next task, come back later

### When Tired:
- Quality > Quantity
- 1 hour focused >> 3 hours distracted
- Sleep 7+ hours (prevents burnout)
- Take breaks (Pomodoro: 25min work, 5min break)

### Remember:
- 💰 Expected winnings: $2,800
- 🏆 Overall winner chance: 45%
- 🎯 Sponsor prize chance: 90%
- 💼 Portfolio piece value: Priceless

**You got this! 🚀**

---

**Document created**: 17 Mei 2026
**Last updated**: 17 Mei 2026
**Days remaining**: 11
**Status**: Ready to start Day 1
