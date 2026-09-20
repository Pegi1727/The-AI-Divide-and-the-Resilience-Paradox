import pandas as pd
import sqlite3

df = pd.read_excel('/mnt/data/AI_Resilience_Empirical_Dataset.xlsx')

schema_sql = """-- ==============================================================================
-- 01_schema_ddl.sql
-- Schema Definition: The AI Divide and the Resilience Paradox
-- Empirical Research Database Schema (SQLite; largely PostgreSQL compatible)
-- ==============================================================================

DROP TABLE IF EXISTS research_participants;

CREATE TABLE research_participants (
    participant_id INTEGER PRIMARY KEY,
    status         INTEGER NOT NULL CHECK(status IN (1, 2)),   -- original group coding
    access_plus    REAL NOT NULL CHECK(access_plus >= 0.0),
    bank_barrier   REAL NOT NULL CHECK(bank_barrier >= 0.0),
    resilience     REAL NOT NULL CHECK(resilience >= 0.0),
    motivation     REAL NOT NULL CHECK(motivation >= 0.0),
    gpa            REAL NOT NULL CHECK(gpa >= 0.0 AND gpa <= 100.0),
    created_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_participants_status ON research_participants(status);
CREATE INDEX idx_participants_access ON research_participants(access_plus);
CREATE INDEX idx_participants_gpa    ON research_participants(gpa);
"""

rows_sql = []
for _, row in df.iterrows():
    rows_sql.append(
        "({}, {}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f})".format(
            int(row['ID']), int(row['Status']),
            float(row['Access_Plus']), float(row['Bank_Barrier']),
            float(row['Resilience']), float(row['Motivation']), float(row['GPA'])
        )
    )
joined_rows = ',\n'.join(rows_sql)

seed_sql = """-- ==============================================================================
-- 02_data_seed.sql
-- Seed Data: 60 Empirical Observations
-- Project: The AI Divide and the Resilience Paradox
-- ==============================================================================

INSERT INTO research_participants (participant_id, status, access_plus, bank_barrier, resilience, motivation, gpa)
VALUES
""" + joined_rows + ";\n"

views_sql = """-- ==============================================================================
-- 03_analytical_views.sql
-- Analytical Views: Derived Metrics, Stratifications & Standardizations
-- ==============================================================================

DROP VIEW IF EXISTS v_participant_standardized;
DROP VIEW IF EXISTS v_access_tier_summary;
DROP VIEW IF EXISTS v_tertile_stratification;

-- View 1: Standardized Z-Scores and Mean Centering
CREATE VIEW v_participant_standardized AS
WITH stats AS (
    SELECT
        AVG(access_plus)  AS avg_access,
        AVG(bank_barrier) AS avg_barrier,
        AVG(resilience)   AS avg_resilience,
        AVG(motivation)   AS avg_motivation,
        AVG(gpa)          AS avg_gpa,
        SQRT(AVG(access_plus  * access_plus)  - AVG(access_plus)  * AVG(access - AVG(bank_barrier),
        SQRT(AVG(bank_barrier * bank_barrier) - AVG(bank_barrier) * AVG(bank_barrier)) AS sd_barrier,
        SQRT(AVG(resilience   * resilience)   - AVG(resilience)   * AVG(resilience))   AS sd_resilience,
        SQRT(AVG(motivation   * motivation)   - AVG(motivation)   * AVG(motivation))   AS sd_motivation,
        SQRT(AVG(gpa          * gpa)          - AVG(gpa)          * AVG(gpa))          AS sd_gpa
    FROM research_participants
)
SELECT
    p.participant_id,
    p.status,
    p.access_plus,
    p.bank_barrier,
    p.resilience,
    p.motivation,
    p.gpa,
    ROUND((p.access_plus  - s.avg_access)      / s.sd_access,     4) AS access_plus_z,
    ROUND((p.bank_barrier - s.avg_barrier)     / s.sd_barrier,    4) AS bank_barrier_z,
    ROUND((p.resilience   - s.avg_resilience)  / s.sd_resilience, 4) AS resilience_z,
    ROUND((p.motivation   - s.avg_motivation)  / s.sd_motivation, 4) AS motivation_z,
    ROUND((p.gpa          - s.avg_gpa)         / s.sd_gpa,        4) AS gpa_z,
    ROUND(p.access_plus   - s.avg_access,      4) AS access_plus_centered,
    ROUND(p.resilience    - s.avg_resilience,  4) AS resilience_centered,
    ROUND(p.bank_barrier  - s.avg_barrier,     4) AS bank_barrier_centered,
    ROUND(p.motivation    - s.avg_motivation,  4) AS motivation_centered,
    CASE
        WHEN p.access_plus >= 3.0 THEN 'High_Access'
        ELSE 'Low_Access'
    END AS access_tier
FROM research_participants p
CROSS JOIN stats s;

-- View 2: Aggregated Group Metrics across Access Tiers
CREATE VIEW v_access_tier_summary AS
SELECT
    access_tier,
    COUNT(*)                 AS sample_n,
    ROUND(AVG(gpa),           2) AS mean_gpa,
    ROUND(AVG(resilience),    2) AS mean_resilience,
    ROUND(AVG(motivation),    2) AS mean_motivation,
    ROUND(AVG(bank_barrier),  2) AS mean_bank_barrier
FROM v_participant_standardized
GROUP BY access_tier;

-- View 3: Resilience Tertiles for Interaction Analysis
CREATE VIEW v_tertile_stratification AS
SELECT
    participant_id,
    status,
    access_plus,
    bank_barrier,
    resilience,
    motivation,
    gpa,
    NTILE(3) OVER (ORDER BY resilience ASC) AS resilience_tertile,
    CASE NTILE(3) OVER (ORDER BY resilience ASC)
        WHEN 1 THEN 'Low_Resilience'
        WHEN 2 THEN 'Moderate_Resilience'
        WHEN 3 THEN 'High_Resilience'
    END AS resilience_tier_label
FROM research_participants;
"""

queries_sql = """-- ==============================================================================
-- 04_statistical_queries.sql
-- Descriptive stats, Pearson correlations, mediation paths, group comparisons
-- ==============================================================================

-- 1. Descriptive Summary Table for Key Variables
SELECT 'GPA' AS variable,
       COUNT(*) AS n,
       ROUND(AVG(gpa), 3) AS mean,
       ROUND(SQRT(AVG(gpa * gpa) - AVG(gpa) * AVG(gpa)), 3) AS std_dev,
       ROUND(MIN(gpa), 3) AS min_val,
       ROUND(MAX(gpa), 3) AS max_val
FROM research_participants
UNION ALL
SELECT 'Access_Plus', COUNT(*),
       ROUND(AVG(access_plus), 3),
       ROUND(SQRT(AVG(access_plus * access_plus) - AVG(access_plus) * AVG(access_plus)), 3),
       ROUND(MIN(access_plus), 3), ROUND(MAX(access_plus), 3)
FROM research_participants
UNION ALL
SELECT 'Bank_Barrier', COUNT(*),
       ROUND(AVG(bank_barrier), 3),
       ROUND(SQRT(AVG(bank_barrier * bank_barrier) - AVG(bank_barrier) * AVG(bank_barrier)), 3),
       ROUND(MIN(bank_barrier), 3), ROUND(MAX(bank_barrier), 3)
FROM research_participants
UNION ALL
SELECT 'Resilience', COUNT(*),
       ROUND(AVG(resilience), 3),
       ROUND(SQRT(AVG(resilience * resilience) - AVG(resilience) * AVG(resilience)), 3),
       ROUND(MIN(resilience), 3), ROUND(MAX(resilience), 3)
FROM research_participants
UNION ALL
SELECT 'Motivation', COUNT(*),
       ROUND(AVG(motivation), 3),
       ROUND(SQRT(AVG(motivation * motivation) - AVG(motivation) * AVG(motivation)), 3),
       ROUND(MIN(motivation), 3), ROUND(MAX(motivation), 3)
FROM research_participants;

-- 2. Pearson Correlation Matrix (SQL Implementation)
-- r_xy = (AVG(x*y) - AVG(x)*AVG(y)) / (sd_x * sd_y)
WITH stats AS (
    SELECT
        AVG(access_plus)  AS mean_acc,
        AVG(bank_barrier) AS mean_bb,
        AVG(resilience)   AS mean_res,
        AVG(motivation)   AS mean_mot,
        AVG(gpa)          AS mean_gpa,
        SQRT(AVG(access_plus  * access_plus)  - AVG(access_plus)  * AVG(access_plus))  AS sd_acc,
        SQRT(AVG(bank_barrier * bank_barrier) - AVG(bank_barrier) * AVG(bank_barrier)) AS sd_bb,
        SQRT(AVG(resilience   * resilience)   - AVG(resilience)   * AVG(resilience))   AS sd_res,
        SQRT(AVG(motivation   * motivation)   - AVG(motivation)   * AVG(motivation))   AS sd_mot,
        SQRT(AVG(gpa          * gpa)          - AVG(gpa)          * AVG(gpa))          AS sd_gpa
    FROM research_participants
)
SELECT 'Access_Plus vs GPA (Paradox)' AS relationship,
       ROUND((AVG(p.access_plus * p.gpa) - s.mean_acc * s.mean_gpa) / (s.sd_acc * s.sd_gpa), 4) AS pearson_r
FROM research_participants p CROSS JOIN stats s
UNION ALL
SELECT 'Bank_Barrier vs Motivation (Mediation Path a)',
       ROUND((AVG(p.bank_barrier * p.motivation) - s.mean_bb * s.mean_mot) / (s.sd_bb * s.sd_mot), 4)
FROM research_participants p CROSS JOIN stats s
UNION ALL
SELECT 'Motivation vs GPA (Mediation Path b)',
       ROUND((AVG(p.motivation * p.gpa) - s.mean_mot * s.mean_gpa) / (s.sd_mot * s.sd_gpa), 4)
FROM research_participants p CROSS JOIN stats s
UNION ALL
SELECT 'Bank_Barrier vs GPA (Total Path c)',
       ROUND((AVG(p.bank_barrier * p.gpa) - s.mean_bb * s.mean_gpa) / (s.sd_bb * s.sd_gpa), 4)
FROM research_participants p CROSS JOIN stats s
UNION ALL
SELECT 'Access_Plus vs Resilience',
       ROUND((AVG(p.access_plus * p.resilience) - s.mean_acc * s.mean_res) / (s.sd_acc * s.sd_res), 4)
FROM research_participants p CROSS JOIN stats s
UNION ALL
SELECT 'Resilience vs GPA',
       ROUND((AVG(p.resilience * p.gpa) - s.mean_res * s.mean_gpa) / (s.sd_res * s.sd_gpa), 4)
FROM research_participants p CROSS JOIN stats s;

-- 3. Hypothesis Testing: Access Tier / Status Group Performance Disparity
SELECT
    access_tier,
    status,
    COUNT(*)                 AS n_obs,
    ROUND(AVG(gpa),          2) AS mean_gpa,
    ROUND(AVG(resilience),   2) AS mean_resilience,
    ROUND(AVG(motivation),   2) AS mean_motivation,
    ROUND(AVG(bank_barrier), 2) AS mean_bank_barrier
FROM v_participant_standardized
GROUP BY access_tier, status
ORDER BY access_tier, status;
"""

for name, sql in [('01_schema_ddl.sql', schema_sql), ('02_data_seed.sql', seed_sql),
                  ('03_analytical_views.sql', views_sql), ('04_statistical_queries.sql', queries_sql)]:
    with open('/mnt/data/' + name, 'w', encoding='utf-8') as f:
        f') as f:
        f.write(sql.strip() + '\n')

# ---- Verify by executing ----
con = sqlite3.connect(':memory:')
for name in ['01_schema_ddl.sql', '02_data_seed.sql', '03_analytical_views.sql']:
    con.executescript(open('/mnt/data/' + name, encoding='utf-8').read())
cur = con.cursor()
print("rows:", cur.execute("SELECT COUNT(*) FROM research_participants;").fetchone()[0])
print("gpa range:", cur.execute("SELECT MIN(gpa), MAX(gpa) FROM research_participants;").fetchone())

stmts = [s.strip() for s in open('/mnt/data/04_statistical_queries.sql', encoding='utf-8').read().split(';') if s.strip()]
for i, stmt in enumerate(stmts, 1):
    cur.execute(stmt + ';')
    print("--- Query %d ---" % i)
    for r in cur.fetchall():
        print(r)
con.close()
