-- Schema Definition: The AI Divide and the Resilience Paradox
-- Standard SQLite & PostgreSQL compatible DDL

DROP VIEW IF EXISTS v_participant_standardized;
DROP VIEW IF EXISTS v_access_tier_summary;
DROP VIEW IF EXISTS v_tertile_stratification;
DROP TABLE IF EXISTS research_participants;

CREATE TABLE research_participants (
    participant_id INTEGER PRIMARY KEY,
    status INTEGER NOT NULL CHECK(status IN (1, 2)),
    access_plus REAL NOT NULL CHECK(access_plus >= 0.0),
    bank_barrier REAL NOT NULL CHECK(bank_barrier >= 0.0),
    resilience REAL NOT NULL CHECK(resilience >= 0.0),
    motivation REAL NOT NULL CHECK(motivation >= 0.0),
    gpa REAL NOT NULL CHECK(gpa >= 0.0 AND gpa <= 100.0)
);

CREATE INDEX idx_participants_status ON research_participants(status);
CREATE INDEX idx_participants_access ON research_participants(access_plus);
CREATE INDEX idx_participants_gpa ON research_participants(gpa);
