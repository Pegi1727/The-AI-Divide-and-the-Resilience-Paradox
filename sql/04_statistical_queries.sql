-- Pure SQL Statistical & Psychometric Queries

-- Query 1: Descriptive Statistics (Mean, SD, Min, Max)
SELECT 'GPA' AS variable, COUNT(*) AS n,
    ROUND(AVG(gpa), 3) AS mean,
    ROUND(SQRT(AVG(gpa * gpa) - AVG(gpa) * AVG(gpa)), 3) AS std_dev,
    ROUND(MIN(gpa), 3) AS min_val, ROUND(MAX(gpa), 3) AS max_val
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

-- Query 2: Pearson Correlation Matrix Derived Entirely in SQL
WITH stats AS (
    SELECT
        AVG(access_plus) AS m_acc, AVG(bank_barrier) AS m_bb,
        AVG(resilience) AS m_res, AVG(motivation) AS m_mot, AVG(gpa) AS m_gpa,
        SQRT(AVG(access_plus * access_plus) - AVG(access_plus) * AVG(access_plus)) AS sd_acc,
        SQRT(AVG(bank_barrier * bank_barrier) - AVG(bank_barrier) * AVG(bank_barrier)) AS sd_bb,
        SQRT(AVG(resilience * resilience) - AVG(resilience) * AVG(resilience)) AS sd_res,
        SQRT(AVG(motivation * motivation) - AVG(motivation) * AVG(motivation)) AS sd_mot,
        SQRT(AVG(gpa * gpa) - AVG(gpa) * AVG(gpa)) AS sd_gpa
    FROM research_participants
)
SELECT 'Access_Plus vs GPA (Paradox)' AS hypothesis_path,
    ROUND((AVG(p.access_plus * p.gpa) - s.m_acc * s.m_gpa) / (s.sd_acc * s.sd_gpa), 4) AS pearson_r
FROM research_participants p CROSS JOIN stats s
UNION ALL
SELECT 'Bank_Barrier vs Motivation (Path a)',
    ROUND((AVG(p.bank_barrier * p.motivation) - s.m_bb * s.m_mot) / (s.sd_bb * s.sd_mot), 4)
FROM research_participants p CROSS JOIN stats s
UNION ALL
SELECT 'Motivation vs GPA (Path b)',
    ROUND((AVG(p.motivation * p.gpa) - s.m_mot * s.m_gpa) / (s.sd_mot * s.sd_gpa), 4)
FROM research_participants p CROSS JOIN stats s
UNION ALL
SELECT 'Bank_Barrier vs GPA (Total Path c)',
    ROUND((AVG(p.bank_barrier * p.gpa) - s.m_bb * s.m_gpa) / (s.sd_bb * s.sd_gpa), 4)
FROM research_participants p CROSS JOIN stats s
UNION ALL
SELECT 'Resilience vs Motivation',
    ROUND((AVG(p.resilience * p.motivation) - s.m_res * s.m_mot) / (s.sd_res * s.sd_mot), 4)
FROM research_participants p CROSS JOIN stats s;

-- Query 3: Access Tier Disparity Group Evaluation
SELECT
    access_tier,
    COUNT(*) AS sample_size,
    ROUND(AVG(gpa), 2) AS mean_gpa,
    ROUND(AVG(resilience), 2) AS mean_resilience,
    ROUND(AVG(motivation), 2) AS mean_motivation,
    ROUND(AVG(bank_barrier), 2) AS mean_bank_barrier
FROM v_participant_standardized
GROUP BY access_tier;
