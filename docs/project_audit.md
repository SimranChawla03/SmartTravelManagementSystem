# Smart Travel Management System — Project Audit Report

## 1. Executive Summary

This audit report documents the current state of the **Smart Travel Management System (STMS)** prior to refactoring, testing, Jira updates, repository publishing, and deployment. The system is an individual Problem-Based Learning (PBL) project built using Python Flask, MongoDB Atlas, HTML5, CSS3, and JavaScript.

---

## 2. Project Architecture & Components

| Component | Technologies / Files | Current State |
|---|---|---|
| **Backend Framework** | Python 3.13.7, Flask 3.1.3, Werkzeug 3.1.9 | Functional; lacks resilient startup error handling for database disconnections. |
| **Database** | MongoDB Atlas (Cluster: `smarttraveldb.pzw2gyd.mongodb.net`, DB: `smart_travel_db`) | Connection verified (`{'ok': 1}`). Indexes present on `users.email` and `bookings.booking_ref`. Collections contain live sample data. |
| **Frontend** | Jinja2 Templates, Vanilla CSS (`static/css/style.css`), Font Awesome / Custom Icons | Fully styled high-fidelity UI; directory casing was initially `Templates/` and `Static/` (normalized to `templates/` and `static/` for Linux production hosting). |
| **Authentication** | Werkzeug password hashing (`scrypt`), Flask session cookie with HTTPOnly and SameSite=Lax | Registration, login, logout, and `@login_required` decorator implemented. Needs DB failure exception handling. |
| **Search & Discovery** | In-memory flight catalogue (`AIRLINE_TEMPLATES`, `DESTINATIONS`) | City-based lookup functional; lacks country-alias fallback; displays empty state when destination is searched without travel date. |
| **Booking & E-Tickets** | Secret token generation (`ST-XXXXXXXX`), MongoDB insert, e-ticket view, booking history | Implemented and connected to MongoDB `bookings` collection. |
| **Testing** | Formerly only single test script `test_db.py`; no automated test suite | No pytest suite or unit/integration test coverage previously existed. |
| **Version Control** | Git 2.50.0 installed locally; repository not initialized; no remotes attached | Not yet initialized; `.gitignore` was minimal and missing IDE/OS exclusions. |
| **Project Management** | Jira project key: `STMS` | No Jira API tokens present in local environment; issue structure and backlog must be generated and audited. |
| **Deployment** | None | No WSGI configuration (Gunicorn installed during audit); no Procfile / render.yaml. |

---

## 3. Detailed Inspection Findings

### 3.1 What Works
1. **MongoDB Connectivity**: Tested against MongoDB Atlas cluster with TLS verification enabled; ping succeeded.
2. **User Authentication Flow**:
   - Registration with input length bounds (name 2–80, password 8–128, email regex check).
   - Password hashing with Werkzeug `generate_password_hash` and `check_password_hash`.
   - Prevention of duplicate user registration via MongoDB unique index on `email`.
   - Session management storing `user_id`, `user_name`, and `user_email`.
   - Safe redirect parameter handling avoiding open redirects.
   - Session destruction on logout with flash notification.
3. **Flight Search & Booking Flow**:
   - Destination catalog with realistic airline schedules, departure/arrival times, fare types, baggage allowances, and calculated pricing.
   - Date validation ensuring travel dates are not in the past (`parse_travel_date`).
   - Traveler count validation (1–5 travelers).
   - Booking record generation with unique reference prefix (`ST-XXXX`).
   - Booking history view (`/my-bookings`) and booking confirmation e-ticket view (`/booking/<ref>`).

### 3.2 What Was Broken or Defective
1. **Case-Sensitivity on Linux / Production (CRITICAL)**:
   - Template and static folders were named `Templates/` and `Static/`. While functioning on case-insensitive Windows filesystems, this causes fatal `TemplateNotFound` and 404 errors on Linux hosting (Render / Docker).
   - *Status*: Folders normalized to lowercase `templates/` and `static/`.
2. **MongoDB Startup & Network Vulnerability**:
   - `client = MongoClient(...)` and `create_index` executed synchronously at module import level. If DNS resolution or internet connection fails, importing `app` throws `ConfigurationError` or `ServerSelectionTimeoutError`, preventing the application or test suites from loading.
   - Route handlers lacked `try...except PyMongoError` blocks, meaning intermittent database drops produce raw HTTP 500 error pages rather than user-friendly flash notifications.
3. **Empty Date Handling in Destination Search**:
   - In `destinations.html`, flight cards only rendered when `destination_info and travel_date` were both truthy. If a user clicked a destination card from the homepage (e.g. London, Paris, Tokyo) which only passes `?destination=London`, no flight results appeared; instead, a generic "Ready to find your flight?" prompt was shown.
4. **Unmatched Search Message Suppression**:
   - When a user searched an invalid or unsupported destination without specifying a date, the template fell through to the initial prompt rather than displaying "No demo flights found for [Query]".
5. **Destination Search by Country**:
   - Destination search only indexed city names (`london`, `paris`, `tokyo`), but the search bar placeholder explicitly states *"Search destinations, countries..."*. Searching "France" or "United Kingdom" yielded no results.

### 3.3 What Needs to Be Tested
1. Registration boundary values (name lengths 1, 2, 80, 81; password lengths 7, 8, 128, 129).
2. Malformed email formats, missing fields, and case normalization.
3. Duplicate registration handling.
4. Login with valid, invalid, and non-existent credentials.
5. Session persistence and `@login_required` protection on `/account`, `/destinations`, `/book`, `/booking/<ref>`, and `/my-bookings`.
6. Destination queries (exact match, case insensitivity, country alias match, whitespace trimming, unmatched queries).
7. Date boundary validation (past dates, current date, future dates, invalid date strings).
8. Traveler bounds (0, 1, 5, 6, non-integer inputs).
9. Booking creation, price calculations (base price * traveler multiplier), and unique reference generation.
10. Behavior when MongoDB connection is unavailable (graceful degradation vs crash).

### 3.4 Requirements for College PBL Evaluation
- Demonstrated implementation of two functional modules:
  1. *Module 1: User Registration and Authentication*
  2. *Module 2: Destination Search and Selection*
- Comprehensive automated test suite with Equivalence Partitioning, Boundary Value Analysis, and Integration tests.
- Defect tracking documentation (Bug report, retesting report).
- Jira project tracking (Epics, User Stories, Tasks, Sprints, Defect tickets) under key `STMS`.
- Clean Git repository with proper `.gitignore`, no committed secrets, published to GitHub.
- Cloud deployment (Render) with live URL and verified functionality.
- Academic documentation: Module descriptions, functional requirements, audit reports, presentation slides, and formal project report.
