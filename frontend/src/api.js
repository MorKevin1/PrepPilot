/**
 * All backend calls go through this file so components never hard-code URLs.
 *
 * Vite only exposes env vars that start with VITE_. If VITE_API_URL is unset,
 * we talk to the local FastAPI server. The browser treats :5173 and :8000 as
 * different origins, so FastAPI must allow CORS for the Vite origin.
 */
const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

async function request(path) {
  const response = await fetch(`${API_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status} ${path}`);
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
