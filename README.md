# PrepPilot

PrepPilot is a practice exam application for studying for certification exams. Choose an exam, focus on a topic, answer multiple-choice questions, and review what you got right and wrong.

Questions in the bank are original practice items. They are not official exam questions.

## Run the API

From `backend`, with Postgres running and a database named `PrepPilot`:

```powershell
copy .env.example .env
.\venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

`.env` holds the database URL and is not committed. `.env.example` is a localhost placeholder.

Load the question bank (safe to run again; existing questions are skipped):

```powershell
.\venv\Scripts\python.exe seed_exam_bank.py
```

If `practice_sessions` does not exist yet, apply `backend/migrations/001_practice_sessions.sql`.

API docs: http://127.0.0.1:8000/docs

## Run the UI

From `frontend`, with the API already running:

```powershell
npm install
npm run dev
```

Open http://localhost:5173. The page calls the API on port 8000.

## What you can do

1. Choose an exam.
2. Choose a topic.
3. Answer the questions. Each choice is saved.
4. On the last question, click Finish.
5. Review the score, the correct choices, and the explanations.
