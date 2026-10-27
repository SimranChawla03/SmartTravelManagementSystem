# Smart Travel Management System — Test Cases and Execution Results

## 1. Test Execution Summary

- **Total Test Cases Defined**: 67
- **Total Tests Executed**: 67
- **Passed**: 64 (Mocked & Unit Tests: 64/64)
- **Failed**: 0
- **Blocked / Skipped**: 3 (Live MongoDB Atlas tests skipped due to dynamic client IP whitelist restriction on Atlas cluster)
- **Success Rate (Executed)**: 100% of executable tests passed.

---

## 2. Test Execution Details

### Module 1: User Registration & Authentication (`tests/test_auth.py`)

| Test Case ID | Module | Test Scenario | Test Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| **TC-AUTH-01** | Auth | Valid User Registration | Name: "Alex Mercer", Email: "alex@example.com", Pass: "Password123!" | Account created, redirected to login with success flash. Password hashed. | Account created, user found in DB with scrypt hash, redirect 200. | **PASS** |
| **TC-AUTH-02** | Auth | BVA: Name Minimum Boundary (2 chars) | Name: "Al", Email: "al@example.com", Pass: "Password123!" | Registration succeeds. | Account created successfully. | **PASS** |
| **TC-AUTH-03** | Auth | BVA: Name Maximum Boundary (80 chars) | Name: 80 "A"s, Email: "a80@example.com", Pass: "Password123!" | Registration succeeds. | Account created successfully. | **PASS** |
| **TC-AUTH-04** | Auth | BVA: Name Below Minimum (1 char) | Name: "A", Email: "a1@example.com", Pass: "Password123!" | Registration rejected with length error message. | Error message displayed; user not inserted. | **PASS** |
| **TC-AUTH-05** | Auth | BVA: Name Above Maximum (81 chars) | Name: 81 "A"s, Email: "a81@example.com", Pass: "Password123!" | Registration rejected with length error message. | Error message displayed; user not inserted. | **PASS** |
| **TC-AUTH-06a** | Auth | EP: Invalid Email (Missing @ and domain) | Email: "notanemail" | Rejected with invalid email error. | Error message displayed; user not inserted. | **PASS** |
| **TC-AUTH-06b** | Auth | EP: Invalid Email (Missing @) | Email: "missingatsign.com" | Rejected with invalid email error. | Error message displayed; user not inserted. | **PASS** |
| **TC-AUTH-06c** | Auth | EP: Invalid Email (Missing user before @) | Email: "@nodomain.com" | Rejected with invalid email error. | Error message displayed; user not inserted. | **PASS** |
| **TC-AUTH-06d** | Auth | EP: Invalid Email (Missing domain name) | Email: "user@.com" | Rejected with invalid email error. | Error message displayed; user not inserted. | **PASS** |
| **TC-AUTH-06e** | Auth | EP: Invalid Email (Missing TLD) | Email: "user@domain" | Rejected with invalid email error. | Error message displayed; user not inserted. | **PASS** |
| **TC-AUTH-06f** | Auth | EP: Invalid Email (Whitespace in address) | Email: "spaces in@domain.com" | Rejected with invalid email error. | Error message displayed; user not inserted. | **PASS** |
| **TC-AUTH-07** | Auth | BVA: Password Below Minimum (7 chars) | Password: 7 chars ("Pass12!") | Rejected with password length error. | Error message displayed; registration blocked. | **PASS** |
| **TC-AUTH-08** | Auth | BVA: Password Minimum Boundary (8 chars) | Password: 8 chars ("Pass123!") | Registration succeeds. | Account created successfully. | **PASS** |
| **TC-AUTH-09** | Auth | BVA: Password Maximum Boundary (128 chars) | Password: 128 characters | Registration succeeds. | Account created successfully. | **PASS** |
| **TC-AUTH-10** | Auth | BVA: Password Above Maximum (129 chars) | Password: 129 characters | Rejected with password maximum length error. | Error message displayed; registration blocked. | **PASS** |
| **TC-AUTH-11** | Auth | Duplicate Email Registration | Email: "jane@example.com" (existing) | Rejected with duplicate account notice. | Flash message: *"An account with this email already exists."* | **PASS** |
| **TC-AUTH-12** | Auth | Valid User Login | Email: "jane@example.com", Pass: "ValidPass123!" | Successful login, session created, redirect to home with greeting. | Session contains user_id and email, welcome message shown. | **PASS** |
| **TC-AUTH-13** | Auth | Invalid Login: Incorrect Password | Email: "jane@example.com", Pass: "WrongPassword!" | Rejected with error notice; session untouched. | Error message displayed; session empty. | **PASS** |
| **TC-AUTH-14** | Auth | Invalid Login: Unregistered Email | Email: "nobody@example.com", Pass: "AnyPassword123!" | Rejected with error notice; session untouched. | Error message displayed; session empty. | **PASS** |
| **TC-AUTH-15** | Auth | User Logout Flow | Active authenticated session | Session cleared, redirected to home with sign-out notice. | Session empty, *"You have been signed out successfully."* shown. | **PASS** |
| **TC-AUTH-16a** | Auth | Protected Route Access: `/account` | Unauthenticated GET request | HTTP 302 redirect to `/login` with prompt. | Redirected to `/login`, prompt displayed. | **PASS** |
| **TC-AUTH-16b** | Auth | Protected Route Access: `/destinations` | Unauthenticated GET request | HTTP 302 redirect to `/login` with prompt. | Redirected to `/login`, prompt displayed. | **PASS** |
| **TC-AUTH-16c** | Auth | Protected Route Access: `/my-bookings` | Unauthenticated GET request | HTTP 302 redirect to `/login` with prompt. | Redirected to `/login`, prompt displayed. | **PASS** |
| **TC-AUTH-17** | Auth | Safe Return URL Redirect after Login | Next URL: `/destinations` | User redirected to `/destinations` after successful login. | Redirected to `/destinations`. | **PASS** |
| **TC-AUTH-18** | Auth | Open Redirect Prevention | Next URL: `https://malicious-site.com` | External redirect disallowed; falls back to homepage (`/`). | Fallback to `/` confirmed. | **PASS** |
| **TC-AUTH-19** | Auth | Database Outage during Registration | MongoDB raises `PyMongoError` | Graceful error flash, no 500 crash. | Flash message: *"Database service is currently unavailable."* | **PASS** |
| **TC-AUTH-20** | Auth | Database Outage during Login | MongoDB raises `PyMongoError` | Graceful error flash, no 500 crash. | Flash message: *"Database service is currently unavailable."* | **PASS** |

---

### Module 2: Destination Search & Selection (`tests/test_search.py`)

| Test Case ID | Module | Test Scenario | Test Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| **TC-SRCH-01** | Search | Search Valid City | Destination: "London" | Matching flights displayed (BA, AI, EK, 6E). | Flight cards for all 4 carriers rendered. | **PASS** |
| **TC-SRCH-02a** | Search | EP: Mixed Casing Query | Destination: "lOnDoN" | Matches London schedules. | London flight cards rendered. | **PASS** |
| **TC-SRCH-02b** | Search | EP: Uppercase Query | Destination: "PARIS" | Matches Paris schedules. | Paris flight cards rendered. | **PASS** |
| **TC-SRCH-02c** | Search | EP: Alternating Casing Query | Destination: "ToKyO" | Matches Tokyo schedules. | Tokyo flight cards rendered. | **PASS** |
| **TC-SRCH-02d** | Search | EP: Leading/Trailing Whitespace | Destination: "   singapore   " | Whitespace stripped, matches Singapore. | Singapore flight cards rendered. | **PASS** |
| **TC-SRCH-03a** | Search | Country Alias: "France" | Destination: "France" | Resolves to Paris destination. | Paris flight options displayed. | **PASS** |
| **TC-SRCH-03b** | Search | Country Alias: "United Kingdom" | Destination: "United Kingdom" | Resolves to London destination. | London flight options displayed. | **PASS** |
| **TC-SRCH-03c** | Search | Country Alias: "UK" | Destination: "UK" | Resolves to London destination. | London flight options displayed. | **PASS** |
| **TC-SRCH-03d** | Search | Country Alias: "Japan" | Destination: "Japan" | Resolves to Tokyo destination. | Tokyo flight options displayed. | **PASS** |
| **TC-SRCH-03e** | Search | Country Alias: "United States" | Destination: "United States" | Resolves to New York destination. | New York flight options displayed. | **PASS** |
| **TC-SRCH-03f** | Search | Country Alias: "USA" | Destination: "USA" | Resolves to New York destination. | New York flight options displayed. | **PASS** |
| **TC-SRCH-03g** | Search | Country Alias: "Thailand" | Destination: "Thailand" | Resolves to Bangkok destination. | Bangkok flight options displayed. | **PASS** |
| **TC-SRCH-03h** | Search | Country Alias: "United Arab Emirates" | Destination: "United Arab Emirates" | Resolves to Dubai destination. | Dubai flight options displayed. | **PASS** |
| **TC-SRCH-03i** | Search | Country Alias: "UAE" | Destination: "UAE" | Resolves to Dubai destination. | Dubai flight options displayed. | **PASS** |
| **TC-SRCH-04** | Search | Unmatched Destination Query | Destination: "Atlantis" | Actionable message *"No demo flights found for “Atlantis”"*. | Notice displayed with recommended cities. | **PASS** |
| **TC-SRCH-05** | Search | Empty Search Query | Destination: "" | Search prompt displayed (*"Ready to find your flight?"*). | Prompt displayed without errors. | **PASS** |
| **TC-SRCH-06** | Search | Valid Future Travel Date | Date: Today + 14 days | Date accepted and populated in search. | Form preserves selected future date. | **PASS** |
| **TC-SRCH-07** | Search | Past Travel Date Rejection | Date: Today - 5 days | Error flash; reset to today. | Flash error shown, date reset to today. | **PASS** |
| **TC-SRCH-08** | Search | Malformed Travel Date String | Date: "invalid-date" | Error flash; reset to today. | Flash error shown, date reset to today. | **PASS** |
| **TC-SRCH-09** | Search | BVA: Traveler Minimum Boundary (1) | Travelers: 1 | Accepted; displays "1 traveler". | Form reflects 1 traveler. | **PASS** |
| **TC-SRCH-10** | Search | BVA: Traveler Maximum Boundary (5) | Travelers: 5 | Accepted; displays "5 travelers". | Form reflects 5 travelers. | **PASS** |
| **TC-SRCH-11a** | Search | BVA: Traveler Below Minimum (0) | Travelers: 0 | Falls back to default of 2 travelers. | Form defaults to 2 travelers. | **PASS** |
| **TC-SRCH-11b** | Search | BVA: Traveler Above Maximum (6) | Travelers: 6 | Falls back to default of 2 travelers. | Form defaults to 2 travelers. | **PASS** |
| **TC-SRCH-11c** | Search | EP: Negative Traveler Count | Travelers: -1 | Falls back to default of 2 travelers. | Form defaults to 2 travelers. | **PASS** |
| **TC-SRCH-11d** | Search | EP: Non-Numeric Traveler Count | Travelers: "abc" | Falls back to default of 2 travelers. | Form defaults to 2 travelers. | **PASS** |
| **TC-SRCH-11e** | Search | EP: Extreme Traveler Count | Travelers: 100 | Falls back to default of 2 travelers. | Form defaults to 2 travelers. | **PASS** |
| **TC-SRCH-12** | Search | Flight Card Details Completeness | Query: "London" | Flight cards include airline code, baggage, stops, and price. | Rendered cards contain all metadata. | **PASS** |

---

### Module 2 Extension: Flight Booking & E-Ticket (`tests/test_booking.py`)

| Test Case ID | Module | Test Scenario | Test Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| **TC-BOOK-01** | Booking | Valid Flight Booking | London, BA flight, 2 travelers | Booking record created in DB, redirect to e-ticket. | Booking saved with status "Confirmed", redirect 302. | **PASS** |
| **TC-BOOK-02** | Booking | Total Fare Calculation | Tokyo, BA flight, 3 travelers | Total price = price_per_traveler * 3. | Computed total matches formula exactly. | **PASS** |
| **TC-BOOK-03** | Booking | Unsupported Destination Booking | Destination: "Narnia" | Rejected with catalog notice. | Flash message: *"Please choose a supported destination..."* | **PASS** |
| **TC-BOOK-04** | Booking | Invalid Flight Option ID | Option ID: "nonexistent-flight-id" | Rejected with unavailable flight class notice. | Flash message: *"That flight class is not available..."* | **PASS** |
| **TC-BOOK-05** | Booking | Past Date Booking Rejection | Travel Date: Today - 3 days | Rejected with date error notice. | Flash message: *"Please select a valid travel date..."* | **PASS** |
| **TC-BOOK-06** | Booking | E-Ticket View Details | Valid booking reference | Boarding pass renders passenger name, route, baggage, fare. | E-ticket page rendered with correct values. | **PASS** |
| **TC-BOOK-07** | Booking | Booking Privacy & Isolation | Access other user's booking ref | Rejected with *"Booking not found."* notice. | Access denied; redirected to `/my-bookings`. | **PASS** |
| **TC-BOOK-08** | Booking | My Bookings Listing | User with 1 booking | Booking card displayed with reference and total. | List rendered with 1 card. | **PASS** |
| **TC-BOOK-09** | Booking | My Bookings Empty State | User with 0 bookings | Empty state call-to-action displayed. | Empty state rendered with "Explore Flights" link. | **PASS** |
| **TC-BOOK-10** | Booking | Database Failure during Booking | MongoDB raises `PyMongoError` | Graceful error notice, no 500 crash. | Flash message: *"Database service is currently unavailable."* | **PASS** |

---

### Live MongoDB Atlas Integration Tests (`tests/test_live_db.py`)

| Test Case ID | Module | Test Scenario | Test Data | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|
| **TC-LIVE-01** | Live DB | MongoDB Atlas TLS Ping | Production cluster connection string | Admin command `ping` returns `{'ok': 1.0}`. | Skipped due to client IP not in current Atlas IP Access List. | **SKIPPED** |
| **TC-LIVE-02** | Live DB | Production Collections Verification | `smart_travel_db` database | Collections `users` and `bookings` present. | Skipped due to client IP not in current Atlas IP Access List. | **SKIPPED** |
| **TC-LIVE-03** | Live DB | Production Index Verification | `users` and `bookings` | Unique indexes on `email_1` and `booking_ref_1`. | Skipped due to client IP not in current Atlas IP Access List. | **SKIPPED** |
