# Smart Travel Management System — College PBL Final Evaluation Checklist

This checklist is structured directly according to the 12 evaluation parameters prescribed for the individual Problem-Based Learning (PBL) software engineering viva and practical demonstration.

---

## 1. Evaluation Demonstration Matrix

| # | Evaluation Requirement | Exact Project Artifact / Reference | Demonstration Procedure for Student | Readiness |
|---|---|---|---|---|
| **1** | **Project Title & Problem Statement** | `docs/project_report.md` (Section 1–2)<br>`docs/project_presentation.md` (Slide 2–3) | State project title: *Smart Travel Management System*. Articulate the problem: fragmentation of international travel booking, complex fare opacity, fragile authentication, and poor schedule comparison. | **100% READY** |
| **2** | **System & Module Description** | `docs/module_description.md`<br>`docs/functional_requirements.md` | Walk through architectural diagram: Flask 3.1 backend, MongoDB Atlas replica set, Jinja2 presentation layer, Gunicorn WSGI. Highlight Module 1 (Auth) and Module 2 (Search & Selection). | **100% READY** |
| **3** | **Jira Project (`STMS`)** | `docs/jira_audit.md`<br>`docs/jira_issues_export.csv` | Present Jira project key `STMS`. Show project settings, team member role, and Agile Scrum configuration. | **100% READY** |
| **4** | **Product Backlog** | `docs/jira_audit.md` (Section 3)<br>`docs/jira_issues_export.csv` | Display product backlog showing 6 Epics (`STMS-E1` to `STMS-E6`) and 12 prioritized User Stories/Tasks. | **100% READY** |
| **5** | **User Stories & Acceptance Criteria** | `docs/jira_audit.md`<br>`docs/functional_requirements.md` | Demonstrate sample user stories (e.g. `STMS-2`, `STMS-5`) showing standard format: *“As a [role], I want [action] so that [benefit]”* with formal acceptance criteria. | **100% READY** |
| **6** | **Implementation of Two Functional Modules** | `app.py` (`/register`, `/login`, `/destinations`, `/book`) | **Live Browser Demo**: (1) Register new traveler, show scrypt hash in MongoDB; (2) Search destinations by city/country; compare 4 airlines; book a seat; inspect generated e-ticket. | **100% READY** |
| **7** | **Source Code & Git Repository** | `app.py`, `templates/`, `static/`, `requirements.txt`, `.gitignore` | Review clean code structure in IDE. Show Git commit history, verified `.gitignore` excluding secrets, and modular test structure. | **100% READY** |
| **8** | **Test Cases & Test Results** | `docs/test_cases_and_results.md`<br>`tests/` (Pytest suite) | Run live test command: `python -m pytest tests/test_auth.py tests/test_search.py tests/test_booking.py -v`. Show 64 passing tests with BVA and EP coverage. | **100% READY** |
| **9** | **Bugs / Issues Recorded in Jira** | `docs/bug_report.md`<br>`docs/jira_issues_export.csv` | Present 8 tracked defect tickets (`STMS-BUG-1` to `STMS-BUG-8`) with severity, priority, steps to reproduce, and root cause analysis. | **100% READY** |
| **10** | **Bug Fixing & Retesting Evidence** | `docs/retesting_report.md`<br>`docs/bug_report.md` | Explain before-and-after fixes: Linux directory casing (`BUG-01`), global flash notification dropping (`BUG-02`), safe return URL destruction (`BUG-03`), and live retesting proof. | **100% READY** |
| **11** | **Final Working Demonstration** | Local: `http://127.0.0.1:5000`<br>Cloud: Render Live URL | Demonstrate full user journey: Home -> Register -> Sign In -> Destination Search ("France") -> Select Emirates Flight -> E-Ticket Boarding Pass -> My Bookings -> Logout. | **100% READY** |
| **12** | **Project Report & Presentation** | `docs/project_report.md`<br>`docs/project_presentation.md` | Submit complete academic project report with title page, abstract, requirements, architecture, test matrices, and deliver slide presentation. | **100% READY** |

---

## 2. Quick Demonstration Commands for Viva

### 1. Execute Automated Test Suite (64 Passing Tests)
```bash
python -m pytest tests/test_auth.py tests/test_search.py tests/test_booking.py -v
```

### 2. Launch Local Application for Demonstration
```bash
python app.py
```
Access at `http://127.0.0.1:5000`.

### 3. Verify Database Connectivity Script
```bash
python test_db.py
```
