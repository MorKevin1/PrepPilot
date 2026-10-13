import { useState } from "react";
import ExamList from "./components/ExamList.jsx";
import Quiz from "./components/Quiz.jsx";
import TopicList from "./components/TopicList.jsx";

/**
 * App owns the two selections that decide which screen is visible:
 *
 *   no exam            → ExamList
 *   exam, no topic     → TopicList
 *   exam and topic     → Quiz (starts POST /sessions for that pair)
 *
 * onSelectTopic works like onSelectExam. TopicList does not start the
 * session itself. It reports the clicked topic, and App renders Quiz.
 * "All topics" clears only the topic, so the exam's topic list comes back.
 */
export default function App() {
  const [selectedExam, setSelectedExam] = useState(null);
  const [selectedTopic, setSelectedTopic] = useState(null);

  let subtitle = "Choose an exam to practice.";
  if (selectedTopic) {
    subtitle = "Answer the practice questions.";
  } else if (selectedExam) {
    subtitle = "Choose a topic to practice.";
  }

  return (
    <main className="page">
      <header className="header">
        <h1>PrepPilot</h1>
        <p>{subtitle}</p>
      </header>
      {selectedExam && selectedTopic ? (
        <Quiz
          exam={selectedExam}
          topic={selectedTopic}
          onBack={() => setSelectedTopic(null)}
        />
      ) : selectedExam ? (
        <TopicList
          exam={selectedExam}
          onBack={() => setSelectedExam(null)}
          onSelectTopic={setSelectedTopic}
        />
      ) : (
        <ExamList onSelectExam={setSelectedExam} />
      )}
    </main>
  );
}
