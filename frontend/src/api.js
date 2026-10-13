/**
 * All backend calls go through this file so components never hard-code URLs.
 *
 * Vite only exposes env vars that start with VITE_. If VITE_API_URL is unset,
 * we talk to the local FastAPI server. The browser treats :5173 and :8000 as
 * different origins, so FastAPI must allow CORS for the Vite origin.
 */
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request(path, { method = "GET", body } = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    method,
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!response.ok) {
    let detail = `Request failed: ${response.status} ${path}`;
    try {
      const payload = await response.json();
      if (typeof payload.detail === "string") {
        detail = payload.detail;
      }
    } catch {
      // Keep the status message when the body is not JSON.
    }
    throw new Error(detail);
  }
  return response.json();
}

/** GET /exams — used by ExamList on first paint. */
export function getExams() {
  return request("/exams");
}

/**
 * GET /exams/{id}/topics — used by TopicList after App has a selected exam.
 * examId comes from the object passed through onSelectExam.
 */
export function getExamTopics(examId) {
  return request(`/exams/${examId}/topics`);
}

/** POST /users — get or create the practice user before a session starts. */
export function getOrCreateUser(email) {
  return request("/users", { method: "POST", body: { email } });
}

/**
 * POST /sessions — draw questions for one exam + topic.
 * The response is the sitting, including questions without answer keys.
 */
export function createSession({ userId, examId, topicId, questionCount = 10 }) {
  return request("/sessions", {
    method: "POST",
    body: {
      user_id: userId,
      exam_id: examId,
      topic_id: topicId,
      question_count: questionCount,
    },
  });
}

/** POST /sessions/{id}/answers — save or replace the choice for one question. */
export function submitAnswer(sessionId, questionId, choiceId) {
  return request(`/sessions/${sessionId}/answers`, {
    method: "POST",
    body: { question_id: questionId, choice_id: choiceId },
  });
}

/** POST /sessions/{id}/complete — lock the sitting and store the score. */
export function completeSession(sessionId) {
  return request(`/sessions/${sessionId}/complete`, { method: "POST" });
}

/** GET /sessions/{id}/review — graded questions, including answer keys. */
export function getSessionReview(sessionId) {
  return request(`/sessions/${sessionId}/review`);
}
