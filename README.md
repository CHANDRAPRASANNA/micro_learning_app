# Micro Learning App — Advanced (React + Flask)

## What is included
- Backend (Flask + SQLite) with:
  - Register / Login endpoints (token stored server-side)
  - Lessons & quizzes
  - Progress tracking per user (timestamped)
  - Leaderboard and daily streak endpoint
- Frontend (React) with:
  - Login / Register UI
  - Dashboard of lessons
  - Lesson viewer + quiz submit
  - Leaderboard
- Pre-seeded SQLite database (backend/database.db) with sample data.

## Run backend
1. Create a Python virtualenv and activate it.
2. `pip install -r requirements.txt`
3. `python seed.py`  (creates database.db with sample data)
4. `python app.py`
Backend will run at `http://127.0.0.1:5000`

## Run frontend
1. `cd frontend`
2. `npm install`
3. `npm start`

## Notes
- Auth tokens are simple UUIDs stored in the Sessions table. Keep this project for learning/demo only.
- If you want a production-ready auth, replace sessions with JWT or OAuth and enable HTTPS.

