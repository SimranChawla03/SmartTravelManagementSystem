# Smart Travel Management System — Cloud Deployment Guide & Runbook

## 1. Executive Summary & Deployment Architecture

This document specifies the production architecture, configuration, secrets management, and deployment runbook for hosting the **Smart Travel Management System (STMS)** on **Render Cloud Application Services** with **MongoDB Atlas**.

```
  +-----------------------------------------------------------------------+
  |                          INTERNET / CLIENTS                           |
  |                        HTTPS (SSL/TLS 1.3)                            |
  +-----------------------------------+-----------------------------------+
                                      |
                                      v
  +-----------------------------------------------------------------------+
  |                           RENDER CLOUD PAAS                           |
  |   +---------------------------------------------------------------+   |
  |   |                  Reverse Proxy & Load Balancer                |   |
  |   +-------------------------------+-------------------------------+   |
  |                                   |                                   |
  |                                   v ($PORT)                           |
  |   +---------------------------------------------------------------+   |
  |   |             WSGI Production Server: Gunicorn 26.2             |   |
  |   |                Command: gunicorn app:app --bind               |   |
  |   +-------------------------------+-------------------------------+   |
  |                                   |                                   |
  |                                   v                                   |
  |   +---------------------------------------------------------------+   |
  |   |                 Flask 3.1.3 Application Layer                 |   |
  |   |    Routes: /, /register, /login, /destinations, /book, etc.   |   |
  |   +-------------------------------+-------------------------------+   |
  |                                   |                                   |
  +-----------------------------------|-----------------------------------+
                                      | Strict TLS Handshake (certifi)
                                      v
  +-----------------------------------------------------------------------+
  |                          MONGODB ATLAS CLOUD                          |
  |      Cluster: smarttraveldb.pzw2gyd.mongodb.net (ReplicaSet)          |
  |      Database: smart_travel_db                                        |
  |      Collections: users, bookings                                     |
  |      Indexes: users(email_1), bookings(booking_ref_1)                 |
  +-----------------------------------------------------------------------+
```

---

## 2. Production Readiness Verification

| Component | Status | Production Hardening Implemented |
|---|---|---|
| **WSGI Server** | **Ready** | Gunicorn 26.2.0 installed; Procfile configured as `web: gunicorn app:app --bind 0.0.0.0:$PORT`. |
| **Directory Casing** | **Ready** | Standardized to lowercase `templates/` and `static/` to prevent Linux `TemplateNotFound` errors. |
| **Port Binding** | **Ready** | Application dynamically resolves `os.environ.get("PORT", 5000)` and binds to `0.0.0.0`. |
| **Secrets & Keys** | **Ready** | `.env` strictly excluded via `.gitignore`; `.env.example` created. Secrets injected via cloud environment variables. |
| **Error Handling** | **Ready** | Resilient `get_db()` and `PyMongoError` exception wrappers prevent uncaught 500 crashes during network spikes. |
| **Automated Testing** | **Ready** | 64/64 pytest automated tests passing (100% pass rate). |

---

## 3. MongoDB Atlas Network Access Configuration

To allow Render's distributed container instances to communicate with your MongoDB Atlas cluster:

1. Log into [MongoDB Atlas Console](https://cloud.mongodb.com).
2. In the left navigation sidebar under **Security**, click **Network Access**.
3. Click **Add IP Address**.
4. To allow cloud instances (whose outgoing IPs vary dynamically), select **Allow Access from Anywhere** (`0.0.0.0/0`).
5. (Optional but recommended): Enter a comment such as `Render Web Service Deployment`.
6. Click **Confirm**. MongoDB Atlas will take 1–2 minutes to deploy the updated firewall rules across your replica set nodes.

> [!NOTE]
> When testing locally from a residential or mobile ISP with dynamic IP assignments, `[SSL: TLSV1_ALERT_INTERNAL_ERROR]` occurs if your current home IP has not been added to Atlas Network Access. Adding your current IP or `0.0.0.0/0` in the Atlas console immediately restores direct connectivity.

---

## 4. Render Step-by-Step Deployment Runbook

### Method A: Automated Deployment via GitHub (Recommended)

1. **Push Clean Code to GitHub**:
   Ensure all changes are committed and pushed to your GitHub repository:
   ```bash
   git push origin main
   ```

2. **Create New Web Service in Render**:
   - Log into [Render Dashboard](https://dashboard.render.com).
   - Click the **New +** button in the top right corner and select **Web Service**.
   - Choose **Build and deploy from a Git repository**.
   - Connect your GitHub account and select `SmartTravelManagementSystem`.

3. **Configure Service Parameters**:
   - **Name**: `smart-travel-management-system`
   - **Region**: Choose the closest region (e.g. Frankfurt, Oregon, Singapore).
   - **Branch**: `main`
   - **Root Directory**: Leave blank (root).
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Instance Type**: `Free`

4. **Set Environment Variables**:
   Under **Environment Variables**, click **Add Environment Variable** and enter:
   | Key | Value | Description |
   |---|---|---|
   | `PYTHON_VERSION` | `3.13.2` | Python version for Render build container |
   | `SECRET_KEY` | *(Generate 64-char random hex)* | Used by Flask for signing session cookies |
   | `MONGODB_URI` | `mongodb+srv://...` | Connection URI from your Atlas dashboard |
   | `DATABASE_NAME` | `smart_travel_db` | Target MongoDB database |

5. **Deploy**:
   - Click **Create Web Service**.
   - Render initiates the container build: cloning repository, installing pinned dependencies from `requirements.txt`, and launching Gunicorn.

---

## 5. Deployment Verification Checklist

Once the build logs output `==> Your service is live at https://<your-subdomain>.onrender.com`:

| Step | Action | Expected Result | Verified |
|---|---|---|---|
| **1. Health Check** | Open `https://<service>.onrender.com/` | Homepage loads with luxury dark UI and destination cards. | [ ] |
| **2. Static Assets** | Check browser DevTools console (F12) | CSS (`style.css`), web fonts, and SVGs load with HTTP 200 (no 404s). | [ ] |
| **3. Registration** | Register a new test account at `/register` | Account created; redirected to `/login` with success banner. | [ ] |
| **4. Authentication** | Sign into the account at `/login` | Successful authentication; session greeting displays traveler name. | [ ] |
| **5. Destination Search** | Search "London", "France", "Tokyo" at `/destinations` | Flight schedules render with BA, Air India, Emirates, IndiGo. | [ ] |
| **6. Booking Creation** | Select flight option and confirm reservation | Booking reference generated (`ST-XXXXXXXX`); redirected to e-ticket. | [ ] |
| **7. E-Ticket View** | Verify digital boarding pass | Passenger name, airline, route, baggage, and fare displayed. | [ ] |
| **8. History Verification** | Navigate to `/my-bookings` | Confirmed booking appears in reverse chronological order. | [ ] |
| **9. Session Logout** | Click Logout in navbar | Session destroyed; redirected to homepage with signed-out banner. | [ ] |
