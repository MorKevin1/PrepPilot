/**
 * Graded sitting from GET /sessions/{id}/review.
 *
 * Props
 * -----
 * review — session payload with correct_count and questions that include
 *          is_correct, selected_choice_id, and explanations.
 * onBack — returns to the topic list.
 */
export default function Review({ review, onBack }) {
  const questions = [...review.questions].sort((a, b) => a.position - b.position);

  return (
    <section>
      <button type="button" className="back-button" onClick={onBack}>
        All topics
      </button>
      <h2 className="section-title">Review</h2>
      <p className="section-copy">
        {review.correct_count ?? 0} of {review.question_count} correct
      </p>
      <ul className="exam-list">
        {questions.map((question) => (
          <li key={question.id} className="exam-card">
            <p className="provider">
              {question.is_correct === true && "Correct"}
              {question.is_correct === false && "Incorrect"}
              {question.is_correct == null && "Not answered"}
              {question.difficulty ? ` · ${question.difficulty}` : ""}
            </p>
            <h2>{question.question_text}</h2>
            <ul className="choice-list">
              {question.choices.map((choice) => {
                const selected = choice.id === question.selected_choice_id;
                let className = "choice-result";
                if (choice.is_correct) className += " choice-correct";
                if (selected && !choice.is_correct) className += " choice-incorrect";
                return (
                  <li key={choice.id} className={className}>
                    {choice.choice_text}
                    {selected ? " · your answer" : ""}
                    {choice.is_correct ? " · correct" : ""}
                  </li>
                );
              })}
            </ul>
            {question.explanation && (
              <p className="explanation">{question.explanation}</p>
            )}
          </li>
        ))}
      </ul>
    </section>
  );
}
