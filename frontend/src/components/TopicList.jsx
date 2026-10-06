import { useEffect, useState } from "react";
import { getExamTopics } from "../api.js";

/**
 * Topics for one exam, from GET /exams/{exam.id}/topics.
 *
 * Props
 * -----
 * exam   — the object App stored after the ExamList click (has id, name, …).
 * onBack — function from App that sets selectedExam back to null.
 *
 * This screen only appears after onSelectExam has run. Topics are not
 * clickable yet; the next step would start a practice session.
 */
export default function TopicList({ exam, onBack }) {
  const [topics, setTopics] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // exam.id is a dependency: if App selected a different exam, fetch again.
  useEffect(() => {
    setLoading(true);
    setError(null);
    getExamTopics(exam.id)
      .then((data) => setTopics(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [exam.id]);

  return (
    <section>
      <button type="button" className="back-button" onClick={onBack}>
        All exams
      </button>
      <h2 className="section-title">{exam.name}</h2>
      <p className="section-copy">Choose a topic to focus on.</p>

      {loading && <p className="status">Loading topics…</p>}
      {error && <p className="status error">Could not load topics. ({error})</p>}
      {!loading && !error && topics.length === 0 && (
        <p className="status">No topics for this exam yet.</p>
      )}
      {!loading && !error && topics.length > 0 && (
        <ul className="exam-list">
          {topics.map((topic) => (
            <li key={topic.id} className="exam-card">
              <h2>{topic.name}</h2>
              <p>{topic.description}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
