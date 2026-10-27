# Smart Travel Management System (STMS)

An enterprise-grade, student Problem-Based Learning (PBL) web application designed for seamless global flight search, comparative schedule discovery, user identity management, and digital e-ticket reservation.

![Python](https://img.shields.io/badge/Python-3.13-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.1.3-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-forestgreen.svg)
![Tests](https://img.shields.io/badge/Tests-64%20Passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/Pass%20Rate-100%25-success.svg)
![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)

---

## 1. Project Overview

The **Smart Travel Management System** is an end-to-end travel platform developed to fulfill college academic PBL requirements in software engineering, project management, automated testing, and DevOps deployment.

The system incorporates two core functional modules:
1. **Module 1: User Registration and Authentication** — Self-service registration, input boundary validation, `scrypt` password hashing, duplicate prevention, session management, and route protection.
2. **Module 2: Destination Search and Selection** — Fast, case-insensitive flight search across 9 global destinations, multi-airline comparison (British Airways, Air India, Emirates, IndiGo), country alias resolution, past-date protection, party size bounding, and instant e-ticket issuance.

---

## 2. Features

- **Modern Luxury UI**: Dark aesthetic typography with responsive styling, smooth micro-interactions, and accessible feedback toasts.
- **Robust Security**:
  - `scrypt` password hashing via Werkzeug security suite.
  - HTTPOnly, SameSite Lax session cookies preventing client-side script inspection.
  - Safe relative redirect validation preventing open redirect exploits.
  - Zero plain-text credentials stored in codebase or repository.
- **Flight Discovery & Airline Schedules**:
  - Real-time catalog queries for London, Paris, Tokyo, Singapore, Dubai, Bangkok, New York, Switzerland, and Italy.
  - Multi-tier airline fare models: Standard Economy, Economy Flex, Economy Saver, and Economy Lite.
  - Full schedule details: Departure, arrival, duration, stops, baggage allowance, and per-traveler pricing.
  - Country name resolution (e.g. searching "France" matches Paris; "UK" matches London; "USA" matches New York).
- **Booking & E-Ticket Pipeline**:
  - Unique booking references generated via cryptographically secure tokens (`ST-XXXXXXXX`).
  - Digital boarding pass e-ticket rendering with full route and party fare summaries.
  - User isolation ensuring private reservation history.
- **Resilient Database Layer**:
  - MongoDB Atlas cluster connectivity with strict TLS verification.
  - Graceful degradation and user-friendly error alerts when database connection drops.

---

## 3. Technology Stack

- **Backend**: Python 3.13.7, Flask 3.1.3, Werkzeug 3.1.9
- **Database**: MongoDB Atlas (`pymongo` 4.19.0, `dnspython` 2.9.0)
- **Frontend**: HTML5, CSS3, Jinja2 template inheritance, Vanilla JavaScript
- **Testing**: `pytest` 9.1.1, `mongomock` 4.3.0
- **WSGI / Production**: `gunicorn` 26.2.0
- **Project Management**: Jira Software (`STMS` project key)
- **Hosting / PaaS**: Render

---

## 4. Project Structure

```
SmartTravelManagementSystem/
├── .env.example                # Template for environment variables (safe for git)
├── .gitignore                  # Comprehensive git exclusion list (excludes .env, venv)
├── Procfile                    # Render/Heroku WSGI start command
├── README.md                   # Project documentation and guide
├── render.yaml                 # Render Infrastructure-as-Code Blueprint
├── requirements.txt            # Python dependencies with pinned versions
├── app.py                      # Core Flask application, controllers & models
├── test_db.py                  # Standalone MongoDB Atlas connectivity diagnostic
├── docs/                       # Comprehensive PBL documentation deliverables
│   ├── bug_report.md           # Defect tracking log (8 genuine bugs documented)
│   ├── deployment.md           # Cloud deployment procedure & verification
│   ├── final_demo_checklist.md # Academic PBL demonstration checklist
│   ├── functional_requirements.md # Functional (FR) & Non-Functional (NFR) specs
│   ├── jira_audit.md           # Jira agile audit & sprint progress report
│   ├── jira_issues_export.csv  # Importable Jira issues CSV (Epics, Stories, Bugs)
│   ├── module_description.md   # Detailed architecture of Module 1 & Module 2
│   ├── project_audit.md        # Initial project inspection & gap analysis
│   ├── project_report.md       # Comprehensive academic PBL final report
│   ├── project_presentation.md # College evaluation presentation slides
│   └── test_cases_and_results.md # 67 test cases with Boundary Value Analysis & EP
├── static/
│   └── css/
│       └── style.css           # Global luxury styling & responsive layout
├── templates/
│   ├── account.html            # User account profile overview
│   ├── base.html               # Master layout with global alerts & navigation
│   ├── booking_confirmation.html # Digital e-ticket boarding pass
│   ├── destinations.html       # Flight search results & comparison cards
│   ├── index.html              # Homepage with hero & journey showcases
│   ├── login.html              # Traveler login form
│   ├── my_bookings.html        # Booking history & active reservations
│   └── register.html           # New traveler onboarding form
└── tests/
    ├── conftest.py             # Pytest fixtures & isolated in-memory DB mocks
    ├── test_auth.py            # 21 test cases for Module 1 (Auth & Registration)
    ├── test_search.py          # 23 test cases for Module 2 (Search, Filters, BVA)
    ├── test_booking.py         # 20 test cases for Booking, Calculations & E-Tickets
    └── test_live_db.py         # Integration test suite for live MongoDB Atlas
```

---

## 5. Local Setup Instructions

### Prerequisites
- Python 3.10+ (tested on Python 3.13)
- Git
- MongoDB Atlas cluster connection string

### Step-by-Step Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/SimranChawla03/SmartTravelManagementSystem.git
   cd SmartTravelManagementSystem
   ```

2. **Create and activate a virtual environment**:
   - **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **macOS / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and provide your secrets:
   ```ini
   SECRET_KEY=your_generated_secret_key_here
   MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/?retryWrites=true&w=majority
   DATABASE_NAME=smart_travel_db
   PORT=5000
   ```

5. **Verify database connectivity**:
   ```bash
   python test_db.py
   ```

6. **Start the local development server**:
   ```bash
   python app.py
   ```
   Open your browser at `http://127.0.0.1:5000`.

---

## 6. Running Automated Tests

STMS includes an automated test suite executed via `pytest`. All 64 unit and functional tests run against an isolated in-memory mock database (`mongomock`), requiring zero network connection or test database cleanup:

```bash
python -m pytest tests/test_auth.py tests/test_search.py tests/test_booking.py -v
```

### Running with Coverage & Detailed Reports:
```bash
python -m pytest tests/ -v -rs
```

---

## 7. Cloud Deployment (Render)

The application is pre-configured for production deployment on Render:

1. Push your repository to GitHub.
2. In Render Dashboard, click **New +** -> **Web Service**.
3. Select your GitHub repository (`SmartTravelManagementSystem`).
4. Configure service settings:
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
5. In **Environment Variables**, add:
   - `SECRET_KEY`: Generate a random 64-character hex string.
   - `MONGODB_URI`: Your MongoDB Atlas cluster connection string.
   - `DATABASE_NAME`: `smart_travel_db`
   - `PYTHON_VERSION`: `3.13.2`
6. In MongoDB Atlas **Network Access**, ensure `0.0.0.0/0` (Allow Access from Anywhere) is added so Render's dynamic IP addresses can establish TLS connections.
7. Click **Deploy Web Service**.

---

## 8. Academic Project Deliverables

All documentation required for college evaluation is located in the `docs/` folder:
- **Audit & Requirements**: `docs/project_audit.md`, `docs/functional_requirements.md`, `docs/module_description.md`
- **Testing & Quality Assurance**: `docs/test_cases_and_results.md`, `docs/bug_report.md`, `docs/retesting_report.md`
- **Project Management**: `docs/jira_audit.md`, `docs/jira_issues_export.csv`
- **DevOps & Verification**: `docs/deployment.md`, `docs/final_demo_checklist.md`
- **Final Evaluation**: `docs/project_report.md`, `docs/project_presentation.md`

---

## 9. License

This project is submitted for individual academic evaluation under the MIT License.
