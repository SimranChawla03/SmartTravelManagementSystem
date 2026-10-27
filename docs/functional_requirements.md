# Smart Travel Management System — Functional & Non-Functional Requirements

## 1. Functional Requirements (FR)

| Req ID | Module | Title | Description | Acceptance Criteria |
|---|---|---|---|---|
| **FR-01** | User Management | Account Registration | The system shall allow new users to register an account with name, email, and password. | Name length 2–80 chars, RFC email format, password 8–128 chars. Password stored as secure hash. |
| **FR-02** | User Management | Duplicate Email Prevention | The system shall reject registration requests using an email address that is already registered. | System displays error message *"An account with this email already exists."* and redirects back to `/register`. |
| **FR-03** | Authentication | User Login | The system shall authenticate existing users using registered email and password. | Valid credentials set session cookies (`user_id`, `user_name`, `user_email`) and redirect to dashboard or safe return URL. |
| **FR-04** | Authentication | Credential Failure Handling | The system shall reject invalid email or password attempts with a non-specific error. | System displays *"Invalid email or password. Please try again."* without revealing which field was incorrect. |
| **FR-05** | Authentication | User Logout | The system shall terminate active user sessions upon logout. | Session cleared completely; user redirected to homepage with confirmation message. |
| **FR-06** | Access Control | Route Protection | The system shall prevent unauthenticated access to private views. | Unauthenticated requests to `/account`, `/destinations`, `/book`, `/my-bookings`, `/booking/<ref>` redirect to `/login` with prompt. |
| **FR-07** | Search & Discovery | Destination Query Processing | The system shall match destinations by city or country name regardless of casing and whitespace. | "london", "LONDON", "  London  ", "United Kingdom", "UK" all return London flight schedules. |
| **FR-08** | Search & Discovery | Unmatched Query Handling | The system shall inform users when a search query yields no matching destinations. | System displays *"No demo flights found for [Query]"* with recommended destinations. |
| **FR-09** | Search & Discovery | Travel Date Validation | The system shall enforce valid dates that are not in the past. | Past dates trigger an error notice and automatically reset to the current date. |
| **FR-10** | Search & Discovery | Traveler Count Bounding | The system shall restrict traveler counts between 1 and 5. | Counts < 1 or > 5 or invalid strings fall back to default of 2 travelers. |
| **FR-11** | Booking & Flight | Multi-Airline Flight Schedule | The system shall display multiple airline options per destination with schedule and baggage details. | Schedule displays airline mark, flight number, departure, arrival, duration, stops, baggage, fare tier, price per traveler, and total party price. |
| **FR-12** | Booking & Flight | Reservation Generation | The system shall generate a confirmed booking with an 11-character reference upon flight selection. | Unique reference in format `ST-XXXXXXXX` created, party price calculated, and record saved to MongoDB. |
| **FR-13** | Booking & Flight | E-Ticket Generation | The system shall render a digital boarding pass / e-ticket for confirmed bookings. | E-ticket displays passenger name, flight number, route, departure/arrival times, travel date, baggage, and total fare. |
| **FR-14** | Booking & Flight | Booking Privacy & Isolation | The system shall prevent travelers from accessing reservations belonging to other users. | Requests for non-owned booking references return a *"Booking not found."* notice. |
| **FR-15** | Booking & Flight | Booking History Overview | The system shall display all historical and active bookings for the logged-in user in reverse chronological order. | All bookings associated with `session["user_id"]` listed on `/my-bookings` with direct link to view e-tickets. |

---

## 2. Non-Functional Requirements (NFR)

| NFR ID | Category | Requirement Description | Implementation Verification |
|---|---|---|---|
| **NFR-01** | **Security** | Passwords must never be stored in plain text or reversible formats. | Werkzeug `generate_password_hash` utilizing `scrypt` key derivation with random salt. |
| **NFR-02** | **Security** | Session cookies must be protected against client-side script inspection and CSRF. | `SESSION_COOKIE_HTTPONLY=True`, `SESSION_COOKIE_SAMESITE="Lax"`. |
| **NFR-03** | **Security** | External open redirect vulnerabilities must be mitigated. | Redirect parameters validated to ensure relative path prefix (`/`) and reject protocol-relative paths (`//`). |
| **NFR-04** | **Reliability** | Database connection disconnections or cluster outages must degrade gracefully. | Connection errors caught (`PyMongoError`), logged, and presented to travelers as friendly alerts without unhandled 500 exceptions. |
| **NFR-05** | **Portability** | Template and asset directory paths must remain compatible with POSIX / Linux servers. | Directory names standardized to lower-case `templates/` and `static/`. |
| **NFR-06** | **Performance** | Database indexes must be maintained for frequently queried fields. | Unique indexes on `users.email` and `bookings.booking_ref`. |
