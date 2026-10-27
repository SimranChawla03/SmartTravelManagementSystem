# Smart Travel Management System — Jira Project Audit (`STMS`)

## 1. Project Management Summary

- **Project Key**: `STMS`
- **Project Name**: Smart Travel Management System
- **Project Lead**: Simran Chawla
- **Methodology**: Agile Scrum
- **Epics Defined**: 6
- **User Stories & Engineering Tasks**: 12
- **Defect Issues Logged**: 8
- **Sprint Organization**: 3 Sprints (Sprint 1 Completed, Sprint 2 Completed, Sprint 3 Active/Closing)

---

## 2. Jira Hierarchy & Epics

| Epic Key | Epic Summary | Status | Linked Deliverables |
|---|---|---|---|
| **STMS-E1** | Project Foundation, Database Architecture & Core Infrastructure | **Done** | Flask 3.1, MongoDB Atlas cluster connection, `.env` config, database indexes. |
| **STMS-E2** | Module 1 — User Registration, Identity & Access Control | **Done** | `/register`, `/login`, `/logout`, scrypt hashing, `@login_required` access control. |
| **STMS-E3** | Module 2 — Destination Discovery, Search & Flight Comparison | **Done** | In-memory airline catalog, search normalization, country aliases, BVA filters. |
| **STMS-E4** | Flight Reservation & Digital E-Ticket Issuance | **Done** | `/book`, price computation, unique reference generator (`ST-XXXXXXXX`), `/booking/<ref>`, `/my-bookings`. |
| **STMS-E5** | Quality Assurance, Defect Tracking & Automated Testing | **Done** | Pytest test suite (64 automated tests, 100% pass rate), bug reports, retesting verification. |
| **STMS-E6** | DevOps, Version Control & Cloud Deployment | **In Progress** | Git repo initialization, `.gitignore`, Gunicorn WSGI, GitHub publishing, Render cloud deployment. |

---

## 3. Product Backlog & User Stories

### Sprint 1: Architecture & Module 1 (Completed)
- **STMS-1 (Story)**: *As a system, I want a resilient MongoDB Atlas connection with index constraints so that user and booking data are securely and consistently persisted.*
  - **Status**: `Done`
  - **Acceptance Criteria**: MongoClient ping verified; `email` and `booking_ref` unique indexes created.
- **STMS-2 (Story)**: *As a new traveler, I want to create an account with my name, email, and password so that I can access personalized booking tools.*
  - **Status**: `Done`
  - **Acceptance Criteria**: Length boundaries (name 2–80, password 8–128) validated; email regex check; scrypt password hashing; duplicate email prevention.
- **STMS-3 (Story)**: *As a registered traveler, I want to sign in securely so that I can access my account.*
  - **Status**: `Done`
  - **Acceptance Criteria**: Hash comparison via `check_password_hash`; session creation with HTTPOnly cookie; safe relative redirect after login.
- **STMS-4 (Story)**: *As an administrator, I want unauthenticated visitors restricted from private pages so that traveler data remains secure.*
  - **Status**: `Done`
  - **Acceptance Criteria**: `@login_required` redirects unauthenticated traffic to `/login` with prompt.

### Sprint 2: Module 2 & Flight Booking (Completed)
- **STMS-5 (Story)**: *As a traveler, I want to search global destinations by city or country so that I can explore available flights.*
  - **Status**: `Done`
  - **Acceptance Criteria**: Search normalizes case and whitespace; country aliases resolve to cities; unmatched queries display helpful suggestions.
- **STMS-6 (Story)**: *As a traveler, I want to compare airline options with schedules, baggage, and fare tiers so that I can select the best option.*
  - **Status**: `Done`
  - **Acceptance Criteria**: Renders British Airways, Air India, Emirates, IndiGo with departure/arrival, stops, duration, and price per passenger.
- **STMS-7 (Story)**: *As a traveler, I want to filter by travel date and passenger count so that flight fares are accurately calculated.*
  - **Status**: `Done`
  - **Acceptance Criteria**: Past dates rejected; passenger count bounded between 1 and 5 (defaults safely to 2).
- **STMS-8 (Story)**: *As a traveler, I want to confirm a flight reservation so that my seat is reserved.*
  - **Status**: `Done`
  - **Acceptance Criteria**: Generates unique `ST-XXXXXXXX` reference; calculates total party fare; saves to `bookings` collection.
- **STMS-9 (Story)**: *As a traveler, I want an e-ticket and booking history dashboard so that I can review my reservations.*
  - **Status**: `Done`
  - **Acceptance Criteria**: Digital boarding pass view; user privacy isolation; reverse-chronological `/my-bookings` list.

### Sprint 3: Testing, Bug Fixing & DevOps (Active / Closing)
- **STMS-10 (Story)**: *As a QA engineer, I want comprehensive automated test coverage across authentication, search, and booking so that regressions are prevented.*
  - **Status**: `Done`
  - **Acceptance Criteria**: 64 passing pytest tests with Boundary Value Analysis, Equivalence Partitioning, and mock database isolation.
- **STMS-11 (Task)**: *As a DevOps engineer, I want the codebase audited for secrets and published to a public GitHub repository.*
  - **Status**: `In Progress`
  - **Acceptance Criteria**: Comprehensive `.gitignore`, `.env` excluded, no committed credentials, repository created and pushed.
- **STMS-12 (Task)**: *As a DevOps engineer, I want the application deployed to cloud hosting (Render) using Gunicorn WSGI.*
  - **Status**: `In Progress`
  - **Acceptance Criteria**: Gunicorn WSGI production server configured; deployment guide prepared; live URL verified.

---

## 4. Jira Defect Tracking (Bugs Logged & Resolved)

| Issue Key | Summary | Severity | Linked Story | Status | Resolution |
|---|---|---|---|---|---|
| **STMS-BUG-1** | Fix folder casing mismatch (`Templates`/`Static` -> `templates`/`static`) | Critical | STMS-12 | **Done** | Fixed & Verified |
| **STMS-BUG-2** | Add missing global flash message container to `base.html` | Major | STMS-3 | **Done** | Fixed & Verified |
| **STMS-BUG-3** | Fix premature `session.clear()` destroying `login_next_url` | Medium | STMS-3 | **Done** | Fixed & Verified |
| **STMS-BUG-4** | Resilient MongoDB initialization avoiding boot crash on network drop | High | STMS-1 | **Done** | Fixed & Verified |
| **STMS-BUG-5** | Add route-level PyMongo exception handling across routes | High | STMS-1 | **Done** | Fixed & Verified |
| **STMS-BUG-6** | Add country alias matching to destination search engine | Medium | STMS-5 | **Done** | Fixed & Verified |
| **STMS-BUG-7** | Display unmatched destination notice when travel date is omitted | Low | STMS-5 | **Done** | Fixed & Verified |
| **STMS-BUG-8** | Default travel date to current date when clicking homepage cards | Medium | STMS-5 | **Done** | Fixed & Verified |

---

## 5. Jira Manual Import Instructions

Because local system environment variables did not contain live Jira cloud API credentials, the entire project structure has been formatted into an industry-standard Jira CSV import file: `docs/jira_issues_export.csv`.

To synchronize these issues with your cloud Jira instance:
1. Navigate to your Jira workspace (e.g. `https://your-domain.atlassian.net`).
2. Click **Jira Settings** (gear icon) -> **System** -> **External System Import**.
3. Select **CSV**.
4. Upload `docs/jira_issues_export.csv`.
5. Select project key `STMS`.
6. Click **Map Fields** (the CSV header names match standard Jira fields: `Issue Type`, `Key`, `Summary`, `Description`, `Status`, `Priority`, `Epic Link`, `Resolution`).
7. Click **Begin Import**. All 26 issues (Epics, Stories, Tasks, and Bugs) will import with exact parent-child links and statuses.
