# Smart Travel Management System (STMS)
## College PBL Final Viva & Project Presentation

---

### Slide 1: Title Slide
# Smart Travel Management System
### Problem-Based Learning (PBL) Software Engineering Project
- **Student Name**: Simran Chawla
- **Course**: Individual PBL in Software Development, Testing & DevOps
- **Jira Project Key**: `STMS`
- **Tech Stack**: Python, Flask, MongoDB Atlas, Pytest, Git, Render

> **Presenter Note**: Welcome the evaluation committee. Introduce yourself and state that this project demonstrates full-stack software development, agile tracking in Jira, automated testing, defect resolution, and cloud deployment.

---

### Slide 2: Problem Statement & Objectives
## Problem Statement & Project Objectives
### The Problem:
- Travel portals are cluttered, lack transparent schedule/baggage comparisons, and break on country searches.
- Traditional student prototypes often lack secure password hashing, suffer from open redirect vulnerabilities, and crash on database drops.

### Core Objectives:
1. **Module 1**: Secure User Registration and Authentication subsystem.
2. **Module 2**: Dynamic Destination Search, Airline Schedule Comparison, and Booking Pipeline.
3. **Agile Management**: Jira backlog, Epics, User Stories, and Sprint tracking under key `STMS`.
4. **Automated Testing**: Comprehensive pytest suite (BVA, EP, Security).
5. **Defect Tracking**: Identify genuine defects, fix root causes, and provide retesting evidence.
6. **DevOps**: Clean Git versioning and Render cloud deployment readiness.

> **Presenter Note**: Emphasize that the project focuses on software craftsmanship, security, test-driven validation, and resilient architecture.

---

### Slide 3: System Architecture
## Multi-Tier Architecture & Technology Stack
- **Client Tier**: Responsive dark luxury UI (HTML5, CSS3, Jinja2 template inheritance).
- **Application Tier**: Python 3.13 + Flask 3.1.3 + Gunicorn 26.2 WSGI production server.
- **Data Tier**: MongoDB Atlas NoSQL cluster with strict TLS certificate verification.
- **Testing & Tooling**: Pytest 9.1, Mongomock 4.3, Git, Jira Software.

```
[Browser Client] <== HTTPS ==> [Gunicorn WSGI / Flask App] <== TLS 1.3 ==> [MongoDB Atlas]
```

> **Presenter Note**: Point out that the architecture separates presentation, business logic, and distributed database storage cleanly.

---

### Slide 4: Module 1 — User Registration & Authentication
## Module 1: User Registration & Security
- **Self-Service Registration (`/register`)**:
  - Full name bounded (2–80 chars).
  - Email format validated via RFC regex (max 254 chars).
  - Password strength enforced (8–128 chars).
  - Password hashed using Werkzeug `scrypt` algorithm with unique salt.
  - Duplicate registration prevented via MongoDB unique index on `email`.
- **Authentication & Sessions (`/login`, `/logout`)**:
  - Constant-time hash verification via `check_password_hash`.
  - HTTPOnly, SameSite Lax session cookies preventing XSS and CSRF token leakage.
  - Safe relative redirect validation preventing open redirect attacks.
- **Access Control (`@login_required`)**:
  - Automatically redirects unauthenticated traffic to `/login` with prompt.

> **Presenter Note**: Highlight that security is built-in from the ground up: no plain-text passwords, protected routes, and safe redirects.

---

### Slide 5: Module 2 — Destination Search & Selection
## Module 2: Destination Search & Flight Comparison
- **Intelligent Query Normalization**:
  - Searches 9 world destinations (London, Paris, Tokyo, Singapore, Dubai, Bangkok, New York, Switzerland, Italy).
  - Case-insensitive and whitespace-trimmed.
  - Country alias mapping: Searching "France" resolves Paris; "UK" resolves London; "USA" resolves New York.
- **Flight & Airline Schedules**:
  - Compares British Airways, Air India, Emirates, IndiGo.
  - Displays departure, arrival, duration, stops, baggage allowance, and fare tier.
  - Dynamic pricing calculation: `Price = base_airline_rate * travelers`.
- **Validation Controls**:
  - Past dates strictly rejected and reset to today.
  - Traveler party count bounded to 1–5 passengers.
- **Booking & E-Tickets**:
  - Confirms flight and issues boarding pass with reference `ST-XXXXXXXX`.
  - User isolation ensures travelers only view their own bookings.

> **Presenter Note**: Demonstrate that search handles messy real-world user queries effortlessly.

---

### Slide 6: Agile Project Management via Jira
## Project Management in Jira (`STMS`)
- **6 Epics Defined**:
  - `STMS-E1`: Architecture & MongoDB Persistence
  - `STMS-E2`: Module 1 — Registration & Identity
  - `STMS-E3`: Module 2 — Destination Search & Comparison
  - `STMS-E4`: Flight Reservation & E-Tickets
  - `STMS-E5`: QA, Automated Testing & Verification
  - `STMS-E6`: DevOps, Git & Cloud Deployment
- **12 User Stories**: Written in standard role-action-benefit syntax with clear acceptance criteria.
- **3 Sprints**: Sprint 1 (Foundations), Sprint 2 (Features), Sprint 3 (Testing & Hardening).
- **Importable Deliverable**: `docs/jira_issues_export.csv` created for 1-click Jira cloud import.

> **Presenter Note**: Mention that every requirement and bug was tracked following industry Agile Scrum standards.

---

### Slide 7: Automated Testing Strategy & Execution
## Quality Assurance & Automated Testing
- **Test Framework**: `pytest` with `mongomock` isolated in-memory database fixtures.
- **Total Test Cases**: 67 defined; **64 executed and passed (100% pass rate)**.
- **Execution Time**: 10.93 seconds with zero regressions.

### Testing Methodologies Applied:
1. **Boundary Value Analysis (BVA)**:
   - Name lengths: 1 (rejected), 2 (accepted), 80 (accepted), 81 (rejected).
   - Password lengths: 7 (rejected), 8 (accepted), 128 (accepted), 129 (rejected).
   - Traveler counts: 0 (default 2), 1 (accepted), 5 (accepted), 6 (default 2).
2. **Equivalence Partitioning (EP)**:
   - Invalid email formats (missing @, missing domain, missing user, spaces).
   - Query case permutations (uppercase, lowercase, mixed, whitespace).
3. **Security & Fault Injection**:
   - Open redirect exploit payloads (`https://malicious-site.com`).
   - PyMongo database outage injection testing.
   - Cross-user e-ticket isolation testing.

> **Presenter Note**: Explain that testing utilized isolated in-memory fixtures so automated tests run deterministically and fast without network flakiness.

---

### Slide 8: Defect Tracking & Bug Fixing
## Defect Identification, Fixing & Retesting
Eight genuine defects were discovered, logged, fixed, and retested:

| Bug ID | Summary | Severity | Status |
|---|---|---|---|
| **BUG-01** | Template/Static folder capitalization broke Linux hosting | Critical | **Fixed & Verified** |
| **BUG-02** | Missing global flash message container dropped alert banners | Major | **Fixed & Verified** |
| **BUG-03** | Premature `session.clear()` destroyed safe return URL on login | Medium | **Fixed & Verified** |
| **BUG-04** | Top-level synchronous MongoDB connection crashed app offline | High | **Fixed & Verified** |
| **BUG-05** | Missing `PyMongoError` handlers produced raw HTTP 500 errors | High | **Fixed & Verified** |
| **BUG-06** | Destination search by country name failed to match cities | Medium | **Fixed & Verified** |
| **BUG-07** | Unmatched destination query without date suppressed warning | Low | **Fixed & Verified** |
| **BUG-08** | Homepage destination cards navigated to blank search state | Medium | **Fixed & Verified** |

> **Presenter Note**: Walk the examiners through 1 or 2 bugs in detail (e.g. BUG-02 or BUG-03) to prove deep technical debugging competence.

---

### Slide 9: DevOps, GitHub & Cloud Deployment
## Version Control & Cloud Deployment
- **Git Repository Sanitization**:
  - Initialized on `main` branch.
  - Strict `.gitignore` excluding `.env`, virtual environment (`venv/`), Python bytecode (`__pycache__/`), and backups.
  - Clean history: Zero passwords, API keys, or database URIs committed.
- **Production Readiness**:
  - Gunicorn 26.2 WSGI server configured in `Procfile`.
  - Dynamic port binding via `$PORT`.
  - `render.yaml` Blueprint created for Render cloud deployment.

> **Presenter Note**: Emphasize security compliance: `.env` is never committed; secrets are injected via cloud environment variables.

---

### Slide 10: Live Demonstration & Walkthrough
## Live System Demonstration
### Demonstration Steps:
1. **Homepage Experience**: Review luxury dark theme and responsive layout.
2. **Module 1 (Auth)**: Register a new account (`alex@example.com`) -> Show scrypt hash in MongoDB -> Sign in -> Inspect session greeting.
3. **Module 2 (Search)**: Search "France" -> System resolves Paris -> Compare British Airways, Air India, Emirates, IndiGo.
4. **Validation Test**: Enter a past travel date -> Observe instant validation notice.
5. **Booking Transaction**: Select flight option -> Generate e-ticket with `ST-XXXXXXXX` reference.
6. **E-Ticket & History**: View digital boarding pass -> Check `/my-bookings` list -> Sign out.

> **Presenter Note**: Switch to live browser window and execute this flow smoothly.

---

### Slide 11: Conclusion & Deliverables
## Conclusion & Submission Deliverables
- **Both functional modules fully implemented and hardened.**
- **64 automated tests passing (100% pass rate).**
- **8 genuine defects tracked, fixed, and retested.**
- **Agile Scrum project documented in Jira under `STMS`.**
- **Clean Git repository prepared with strict secrets exclusion.**
- **Comprehensive documentation delivered in `docs/`:**
  - Project Audit, Module Descriptions, Functional Requirements.
  - Test Cases & Results, Bug Report, Retesting Report.
  - Jira Audit, Deployment Guide, Final Demo Checklist.
  - Complete Academic Project Report & Presentation Slides.

### Thank You!
**Questions & Answers**
