# Smart Travel Management System — Module Descriptions

## Overview

The Smart Travel Management System (STMS) is developed as an academic Problem-Based Learning (PBL) project. For evaluation, two primary functional modules have been fully verified, hardened, and tested:

1. **Module 1: User Registration and Authentication**
2. **Module 2: Destination Search and Selection**

---

## Module 1: User Registration and Authentication

### 1. Purpose & Scope
Module 1 manages traveler identity lifecycle, session creation, credential security, and route protection. It provides secure self-service onboarding for new travelers, ensures data integrity, and restricts access to authenticated-only features (such as searching flights, booking tickets, and viewing personal booking history).

### 2. Functional Components
- **Registration Controller (`/register`)**:
  - Accepts full name, email, and password via HTTP POST.
  - Validates full name length (2 to 80 characters).
  - Validates email address syntax using RFC-compliant regular expressions and maximum length constraint (254 characters).
  - Validates password length (8 to 128 characters).
  - Hashes passwords using Werkzeug's `generate_password_hash` (`scrypt` key derivation function with random salt).
  - Enforces email uniqueness at both application logic and database index level (`email_1` unique index in MongoDB).
  - Provides instant feedback using flash messages with category tags (`success`, `error`).
- **Login Controller (`/login`)**:
  - Authenticates credentials against stored password hashes using constant-time comparison (`check_password_hash`).
  - Supports safe relative redirect paths (`?next=/destinations`) and actively rejects external or protocol-relative open redirect attacks (`https://...` or `//...`).
  - Initializes session state containing `user_id`, `user_name`, and `user_email`.
- **Session Management**:
  - Secure HTTPOnly cookie configuration (`SESSION_COOKIE_HTTPONLY=True`).
  - Cross-site request mitigation via SameSite Lax cookie policy (`SESSION_COOKIE_SAMESITE="Lax"`).
- **Logout Controller (`/logout`)**:
  - Clears session storage upon POST request and redirects to homepage with feedback.
- **Access Control Decorator (`@login_required`)**:
  - Intercepts requests to protected endpoints (`/account`, `/destinations`, `/book`, `/booking/<ref>`, `/my-bookings`).
  - Redirects unauthenticated users to `/login` while capturing the intended destination URL.

### 3. Data Model (`users` collection)
```json
{
  "_id": "ObjectId('...')",
  "name": "Jane Traveler",
  "email": "jane@example.com",
  "password_hash": "scrypt:32768:8:1$...",
  "created_at": "ISODate('2026-10-27T11:00:00Z')"
}
```

---

## Module 2: Destination Search and Selection

### 1. Purpose & Scope
Module 2 enables authenticated travelers to discover travel destinations, compare sample flights across multiple commercial airlines, evaluate transparent pricing and baggage rules, filter by date and passenger count, and proceed to booking.

### 2. Functional Components
- **Destination Discovery & Filtering (`/destinations`)**:
  - Queries supported global cities (`London`, `Paris`, `Tokyo`, `Singapore`, `Dubai`, `Bangkok`, `New York`, `Switzerland`, `Italy`).
  - Normalizes input queries with whitespace trimming and case-insensitive matching (`casefold()`).
  - Provides country alias lookups (e.g. searching "France" matches Paris; "UK" / "United Kingdom" matches London; "USA" matches New York; "UAE" matches Dubai).
  - Handles unmatched search terms cleanly by presenting actionable recommendations ("No demo flights found for [Query]").
  - Automatically defaults travel dates to the current date if omitted from search cards, providing zero-click availability for homepage cards.
- **Travel Date Validation**:
  - Rejects past dates (`parse_travel_date` returns None for dates prior to today).
  - Rejects invalid date formats or malformed strings.
  - HTML5 calendar input bounded by `min="{{ today }}"`.
- **Traveler Count Normalization (`get_travelers`)**:
  - Enforces valid passenger boundaries (1 to 5 passengers).
  - Safely falls back to default (2 passengers) for non-integer or out-of-bounds queries.
- **Flight & Airline Schedule Comparison**:
  - Dynamically calculates price per passenger and aggregate party total based on airline fare type and price factors.
  - Displays departure time, arrival time, flight duration, stops, baggage allowance, and fare tier (Standard Economy, Economy Flex, Economy Saver, Economy Lite).
- **Booking Selection Bridge (`/book`)**:
  - Validates selected flight option against destination catalog.
  - Generates cryptographically pseudorandom booking references (`ST-XXXXXXXX`).
  - Commits confirmed reservations into MongoDB Atlas.
  - Dispatches traveler directly to the generated e-ticket view.

### 3. Data Model (`bookings` collection)
```json
{
  "_id": "ObjectId('...')",
  "booking_ref": "ST-9D757B6F",
  "user_id": "6ae08688fc478efa8795502f",
  "user_email": "jane@example.com",
  "user_name": "Jane Traveler",
  "destination": "Tokyo",
  "country": "Japan",
  "travel_date": "2026-11-10",
  "travelers": 2,
  "option_id": "tokyo-ba",
  "travel_name": "British Airways",
  "airline": "British Airways",
  "flight_number": "BA 199",
  "departure": "10:25",
  "arrival": "16:40",
  "duration": "9h 45m",
  "stops": "Non-stop",
  "baggage": "23 kg checked",
  "fare_type": "Standard Economy",
  "travel_type": "Flight",
  "price_per_traveler": 750,
  "total_price": 1500,
  "currency": "USD",
  "status": "Confirmed",
  "created_at": "ISODate('2026-10-27T11:15:00Z')"
}
```
