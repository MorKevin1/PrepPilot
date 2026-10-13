import { useState } from "react";
import ExamList from "./components/ExamList.jsx";
import TopicList from "./components/TopicList.jsx";

export default function App() {
  const [selectedExam, setSelectedExam] = useState(null);

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
/**
 * App is the parent. It owns "which exam is selected?" so the two child
 * screens can stay simple:
 *
 *   selectedExam === null  → show ExamList (the catalog)
 *   selectedExam === {id, name, ...}  → show TopicList for that exam
 *
 * onSelectExam flow (child → parent → other child)
 * -----------------------------------------------
 * 1. App renders <ExamList onSelectExam={setSelectedExam} />.
 *    That passes App's state setter into ExamList as a prop named onSelectExam.
 *    setSelectedExam and onSelectExam are the same function.
 *
 * 2. User clicks AWS SAA. ExamList runs onSelectExam(exam), which is
 *    setSelectedExam(exam). React re-renders App with selectedExam filled in.
 *
 * 3. The ternary below now renders TopicList and hands it that exam object.
 *    TopicList uses exam.id to call GET /exams/{id}/topics.
 *
 * 4. "All exams" calls onBack={() => setSelectedExam(null)}. State goes back
 *    to null and ExamList appears again.
 *
 * Why the function lives in App: ExamList must not hide itself. It only
 * reports "the user picked this exam." App decides what to show next.
 */