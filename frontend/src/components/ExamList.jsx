import { useEffect, useState } from "react";
import { getExams } from "../api.js";

/**
 * Catalog of exams from GET /exams.
 *
 * Props
 * -----
 * onSelectExam(exam) — function provided by App (it is setSelectedExam).
 *   We call it with the full exam object from the API so App can store it
 *   and switch to TopicList. This component does not navigate itself.
 */
export default function ExamList({ onSelectExam }) {
  const [exams, setExams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // [] = run once after the first paint, not on every render.
  useEffect(() => {
    getExams()
      .then((data) => setExams(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="status">Loading exams…</p>;
  }

  if (error) {
    return (
      <p className="status error">
        Could not load exams. Is the API running on port 8000? ({error})
      </p>
    );
  }

  if (exams.length === 0) {
    return <p className="status">No exams in the bank yet.</p>;
  }

  return (
    <ul className="exam-list">
      {exams.map((exam) => (
        <li key={exam.id}>
          <button
            type="button"
            className="exam-card exam-card-button"
            // Arrow function so we pass *this* exam, not the click event.
            onClick={() => onSelectExam(exam)}
          >
            <h2>{exam.name}</h2>
            <p className="provider">{exam.provider}</p>
            <p>{exam.description}</p>
          </button>
        </li>
      ))}
    </ul>
  );
}
