function App() {
  const [selectedExam, setSelectedExam] = React.useState(null);

  return (
    <main className="page">
      <header className="header">
        <h1>PrepPilot</h1>
        <p>
          {selectedExam
            ? "Choose a topic to practice."
            : "Choose an exam to practice."}
        </p>
      </header>
      {selectedExam ? (
        <TopicList exam={selectedExam} onBack={() => setSelectedExam(null)} />
      ) : (
        <ExamList onSelectExam={setSelectedExam} />
      )}
    </main>
  );
}
