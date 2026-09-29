ALTER TABLE questions
    ADD COLUMN IF NOT EXISTS source_type VARCHAR(50),
    ADD COLUMN IF NOT EXISTS source_name VARCHAR(255),
    ADD COLUMN IF NOT EXISTS source_url TEXT,
    ADD COLUMN IF NOT EXISTS license VARCHAR(255);

CREATE TABLE IF NOT EXISTS practice_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users (id),
    exam_id INTEGER NOT NULL REFERENCES exams (id),
    topic_id INTEGER NOT NULL REFERENCES topics (id),
    status VARCHAR(50) NOT NULL DEFAULT 'in_progress',
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    question_count INTEGER NOT NULL,
    correct_count INTEGER
);

CREATE TABLE IF NOT EXISTS practice_session_questions (
    id SERIAL PRIMARY KEY,
    session_id INTEGER NOT NULL REFERENCES practice_sessions (id),
    question_id INTEGER NOT NULL REFERENCES questions (id),
    position INTEGER NOT NULL,
    CONSTRAINT uq_session_question UNIQUE (session_id, question_id)
);

ALTER TABLE question_attempts
    ADD COLUMN IF NOT EXISTS session_id INTEGER REFERENCES practice_sessions (id);

CREATE UNIQUE INDEX IF NOT EXISTS uq_attempt_session_question
    ON question_attempts (session_id, question_id)
    WHERE session_id IS NOT NULL;
