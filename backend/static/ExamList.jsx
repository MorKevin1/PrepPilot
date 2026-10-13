function ExamList({ onSelectExam }) {
  const [exams, setExams] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    fetch("/exams")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Request failed: " + response.status);
        }
        return response.json();
      })
      .then((data) => setExams(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p className="status">Loading exams…</p>;
  }

  if (error) {
    return <p className="status error">Could not load exams. ({error})</p>;
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
