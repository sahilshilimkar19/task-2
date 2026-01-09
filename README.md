Task 2: Two-Dashboard AI Feedback System
# Task 2 – Two-Dashboard AI Feedback System (Web-Based)

This project implements a production-style web application with two dashboards:
1. User Dashboard (public-facing)
2. Admin Dashboard (internal-facing)

Both dashboards communicate with a shared backend service that:
- Stores all submissions
- Uses an LLM to generate responses, summaries, and recommended actions

The system is fully deployed using:
- Backend → Render
- Frontend dashboards → Vercel

This satisfies all constraints mentioned in the assignment.

---

## 🚀 Live Deployments

### ✅ User Dashboard (Public)
Deployed on Vercel  
URL: <PASTE_USER_DASHBOARD_URL>

Users can:
- Select rating (1–5)
- Enter review
- Submit feedback
- View AI-generated response

---

### ✅ Admin Dashboard (Internal)
Deployed on Vercel  
URL: <PASTE_ADMIN_DASHBOARD_URL>

Admins can:
- View all submissions
- See rating, review text
- See AI summary
- See AI-recommended business action
- Dashboard auto-refreshes every few seconds

---

### ✅ Backend API
Deployed on Render  
URL: <PASTE_BACKEND_RENDER_URL>

Backend exposes:
- POST `/submit-review`
- GET `/admin/submissions`

All LLM calls happen server-side as required.

---

## 🏗️ System Architecture



User Dashboard (Vercel) ─┐
├──> FastAPI Backend (Render) ───> OpenRouter LLM API
Admin Dashboard (Vercel) ─┘
└──> Persistent Database (SQLite / PostgreSQL)


- Both dashboards use REST APIs
- Backend handles validation, AI calls, and storage
- Frontend only sends/receives JSON (no LLM access from browser)

---

## 🧠 AI Usage (Mandatory Requirement)

LLM is used for:

1. User-facing response
2. Review summarization
3. Recommended business action

All prompts are generated on the backend and sent to OpenRouter API.

Environment variable used:



OPENROUTER_API_KEY


Configured securely on Render and not exposed in frontend code.

---

## 🧩 Backend Implementation

### Framework
- FastAPI (Python)

### API Endpoints

#### POST `/submit-review`

Request Body:
```json
{
  "rating": 4,
  "review": "Food was great but service was slow."
}


Response:

{
  "message": "Submitted",
  "ai_response": "Thank you for your feedback..."
}


Validations:

Empty review → rejected

Overly long review → rejected

LLM failures → handled gracefully

LLM prompts:

Polite user response

One-line summary

Business recommendation

GET /admin/submissions

Response:

[
  {
    "rating": 4,
    "review": "Food was great...",
    "summary": "Positive food but slow service.",
    "action": "Improve service response time."
  }
]

Database

Option used:

SQLite for quick persistence during deployment
(For production, PostgreSQL can be easily substituted)

SQLAlchemy ORM used to define schema and persist submissions.

🎨 Frontend Implementation
Technology

Plain HTML, CSS, JavaScript (no frameworks)

Fetch API used to call backend

User Dashboard Features

Rating dropdown (1–5)

Review textarea

Submit button

Displays AI-generated response

Displays success or error state

All requests go to:

POST /submit-review

Admin Dashboard Features

Auto-refresh every 5 seconds

Displays:

Rating

Review text

AI summary

Recommended action

Clean card-based UI

All data loaded from:

GET /admin/submissions

☁️ Deployment Strategy
Backend → Render

Steps:

Backend pushed to GitHub repository

Render Web Service created

Build Command:

pip install -r requirements.txt


Start Command:

uvicorn main:app --host 0.0.0.0 --port $PORT


Environment Variable added:

OPENROUTER_API_KEY


Service deployed and tested using /docs

Frontends → Vercel

For both dashboards:

Steps:

Frontend folders pushed to GitHub

New Vercel project created for each dashboard

Root directory set to:

frontend-user for user dashboard

frontend-admin for admin dashboard

Backend API URL configured in JavaScript fetch calls

Deployed as static sites

⚠️ Error Handling

The system gracefully handles:

Empty reviews

Excessively long reviews

LLM API failures

Backend downtime

User receives clear error messages when submission fails.

Admin dashboard continues polling even if backend temporarily fails.
