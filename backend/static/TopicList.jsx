function TopicList({ exam, onBack }) {
  const [topics, setTopics] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState(null);

  React.useEffect(() => {
    setLoading(true);
    setError(null);
    fetch("/exams/" + exam.id + "/topics")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Request failed: " + response.status);
        }
        return response.json();
      })
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
