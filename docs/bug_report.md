# Smart Travel Management System — Defect Tracking & Bug Report

## Overview
This document records genuine defects identified during code inspection, static analysis, unit testing, and cross-platform verification of the Smart Travel Management System.

---

### Defect Log

#### BUG-01: Case-Sensitive Template and Static Asset Directories
- **Bug ID**: `BUG-01`
- **Module**: Deployment & Cross-Platform Compatibility
- **Severity**: Critical
- **Priority**: High
- **Description**: The template and static resource directories were named `Templates` and `Static` with initial capital letters. While functional on Windows' case-insensitive NTFS filesystem, Flask on Linux (e.g. Render, Ubuntu, Docker) defaults to looking for `templates/` and `static/`. This causes immediate `jinja2.exceptions.TemplateNotFound` crashes and 404 errors for CSS on deployment.
- **Steps to Reproduce**:
  1. Deploy application to a Linux container or execute Flask with POSIX filesystem semantics.
  2. Attempt to load `/` or any route.
- **Expected Result**: Templates render and static stylesheets load successfully.
- **Actual Result**: `TemplateNotFound: index.html` thrown; application crashes.
- **Resolution**: Renamed directories to lowercase `templates` and `static`, and explicitly specified `template_folder="templates", static_folder="static"` in `Flask(__name__)`.
- **Status**: Fixed & Retested (Verified).

---

#### BUG-02: Silent Suppression of Flashed Messages Across Core Routes
- **Bug ID**: `BUG-02`
- **Module**: Presentation / User Feedback (Base Template)
- **Severity**: Major
- **Priority**: High
- **Description**: While `login.html` and `register.html` contained localized flash loops, `base.html` lacked a global flash message container. Consequently, any flash messages dispatched when redirecting to `/` (e.g. *"Welcome back!"*, *"You have been signed out successfully."*), `/destinations` (e.g. *"Please choose a valid date that is not in the past."*), or `/my-bookings` (e.g. *"Booking not found."*) were silently swallowed and never rendered.
- **Steps to Reproduce**:
  1. Log into the system.
  2. User is redirected to `/` (home).
  3. Observe that no welcome greeting is rendered on the homepage.
  4. Enter a past travel date on `/destinations`.
  5. Observe that the user is not notified why the date changed.
- **Expected Result**: Prominent alert banners render at the top of the viewport for all redirected flash messages.
- **Actual Result**: No message was presented; feedback was dropped.
- **Resolution**: Embedded an accessible, conditional `flash-container` block in `templates/base.html` styled using existing `.flash-message.success` and `.flash-message.error` CSS rules.
- **Status**: Fixed & Retested (Verified across 10 pytest test cases).

---

#### BUG-03: Premature Session Invalidation Destroying Safe Return URL
- **Bug ID**: `BUG-03`
- **Module**: Module 1 — User Authentication (`/login`)
- **Severity**: Medium
- **Priority**: Medium
- **Description**: In the POST handler of `/login`, `session.clear()` was called before retrieving `session.pop("login_next_url", "")`. Clearing the session dictionary purged the intended destination URL, causing the login controller to always fall back to redirecting to the homepage (`/`) instead of the protected page the user originally requested.
- **Steps to Reproduce**:
  1. As an unauthenticated traveler, visit `/destinations`.
  2. System stores `/destinations` in `session["login_next_url"]` and redirects to `/login`.
  3. Submit valid login credentials.
- **Expected Result**: User is authenticated and automatically forwarded to `/destinations`.
- **Actual Result**: User was redirected to `/` (home).
- **Resolution**: Extracted `next_url = session.get("login_next_url", "")` prior to executing `session.clear()`, preserving the safe return path.
- **Status**: Fixed & Retested (Verified via `test_tc_auth_17_safe_login_redirect`).

---

#### BUG-04: Unhandled Synchronous MongoDB Initialization Crashing App on Import
- **Bug ID**: `BUG-04`
- **Module**: Infrastructure & Database Connectivity
- **Severity**: High
- **Priority**: High
- **Description**: `app.py` previously executed `client = MongoClient(...)` and `create_index(...)` synchronously in the module global scope. If DNS resolution (SRV record lookup) was delayed or internet access was temporarily disconnected, importing `app.py` raised unhandled `pymongo.errors.ConfigurationError` or `ServerSelectionTimeoutError`, causing test suites, development servers, and WSGI workers to crash immediately upon launch.
- **Steps to Reproduce**:
  1. Disconnect network or run in a sandbox without external DNS access.
  2. Execute `python -c "import app"`.
- **Expected Result**: Application module imports cleanly and handles connectivity gracefully.
- **Actual Result**: Process crashed with `pymongo.errors.ConfigurationError: All nameservers failed to answer query...`.
- **Resolution**: Implemented resilient `get_db()` and `init_db_indexes()` functions that catch `PyMongoError` and `ConfigurationError`, log descriptive warnings, and permit offline startup and test mocking.
- **Status**: Fixed & Retested (Verified in sandboxed Python imports and test suite).

---

#### BUG-05: Missing Database Exception Handlers Leading to HTTP 500 Pages
- **Bug ID**: `BUG-05`
- **Module**: Module 1 & Module 2 Database Integration
- **Severity**: High
- **Priority**: High
- **Description**: Route handlers (`/register`, `/login`, `/book`, `/my-bookings`) did not catch `PyMongoError`. If MongoDB Atlas experienced intermittent connectivity hiccups or write timeouts, Flask produced a raw internal server error (HTTP 500) rather than a graceful user-facing notification.
- **Steps to Reproduce**:
  1. Simulate database cluster timeout during registration or booking.
- **Expected Result**: Informative message informing the traveler to try again shortly.
- **Actual Result**: Unhandled PyMongo exception resulting in Werkzeug HTTP 500 error page.
- **Resolution**: Wrapped all database operations with `try...except PyMongoError`, logging the event and flashing *"Database service is currently unavailable. Please try again shortly."*.
- **Status**: Fixed & Retested (Verified via `test_tc_auth_19`, `test_tc_auth_20`, and `test_tc_book_10`).

---

#### BUG-06: Search by Country Name Failing Despite Search Bar Prompt
- **Bug ID**: `BUG-06`
- **Module**: Module 2 — Destination Search
- **Severity**: Low
- **Priority**: Medium
- **Description**: The homepage search bar placeholder states *"Search destinations, countries..."*, but `find_destination()` only matched dictionary keys corresponding to city names (`london`, `paris`, `tokyo`). Searching for "France", "United Kingdom", "Japan", or "United States" returned no flight options.
- **Steps to Reproduce**:
  1. On `/destinations`, type "France" into the search box and submit.
- **Expected Result**: System resolves France to Paris and displays flight options.
- **Actual Result**: Displayed "No demo flights found for “France”".
- **Resolution**: Added a `COUNTRY_ALIASES` mapping and country fallback in `find_destination()` that matches country names and standard abbreviations (e.g. UK, USA, UAE).
- **Status**: Fixed & Retested (Verified via `test_tc_srch_03_country_alias_search` across 9 variations).

---

#### BUG-07: Unmatched Destination Query Without Date Suppressing Notice
- **Bug ID**: `BUG-07`
- **Module**: Module 2 — Destination Search Template
- **Severity**: Low
- **Priority**: Low
- **Description**: In `templates/destinations.html`, the conditional check for unmatched queries was `{% elif destination_query and travel_date %}`. When an unsupported destination was searched without entering a date, the template fell through to the initial prompt (*"Ready to find your flight?"*) rather than informing the user that the destination was not found.
- **Steps to Reproduce**:
  1. Visit `/destinations?destination=Atlantis` without `travel_date`.
- **Expected Result**: Displays *"No demo flights found for “Atlantis”"*.
- **Actual Result**: Displayed *"Ready to find your flight?"*.
- **Resolution**: Changed condition to `{% elif destination_query %}`.
- **Status**: Fixed & Retested (Verified via `test_tc_srch_04_unmatched_destination_query`).

---

#### BUG-08: Homepage Destination Cards Navigating to Blank Search State
- **Bug ID**: `BUG-08`
- **Module**: Module 2 — Destination Search
- **Severity**: Medium
- **Priority**: Medium
- **Description**: Destination cards on the homepage linked to `/destinations?destination=London` without passing a `travel_date`. Because `destinations.html` required both `destination_info` and `travel_date` to render flight cards, clicking on London, Paris, or Tokyo produced an empty results container.
- **Steps to Reproduce**:
  1. Click the arrow button on the London destination card on the homepage.
- **Expected Result**: Available demo flights to London are displayed immediately.
- **Actual Result**: Empty state displayed prompting user to re-enter search details.
- **Resolution**: Updated `destinations()` in `app.py` to automatically default `travel_date` to the current date (`date.today().isoformat()`) when viewing a supported destination.
- **Status**: Fixed & Retested (Verified via `test_tc_srch_01_search_valid_city`).
