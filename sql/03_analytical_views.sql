-- Analytical Views: Standardization, Groupings & Stratifications

DROP VIEW IF EXISTS v_participant_standardized;
DROP VIEW IF EXISTS v_access_tier_summary;
DROP VIEW IF EXISTS v_tertile_stratification;

-- View 1: Standardized Z-Scores and Mean-Centered Variables
CREATE VIEW v_participant_standardized AS
WITH stats AS (
    SELECT
        AVG(access_plus) AS mean_acc,
        AVG(bank_barrier) AS mean_bb,
        AVG(resilience) AS mean_res,
        AVG(motivation) AS mean_mot,
        AVG(gpa) AS mean_gpa,
        SQRT(AVG(access_plus * access_plus) - AVG(access_plus) * AVG(access_plus)) AS sd_acc,
        SQRT(AVG(bank_barrier * bank_barrier) - AVG(bank_barrier) * AVG(bank_barrier)) AS sd_bb,
        SQRT(AVG(resilience * resilience) - AVG(resilience) * AVG(resilience)) AS sd_res,
        SQRT(AVG(motivation * motivation) - AVG(motivation) * AVG(motivation)) AS sd_mot,
        SQRT(AVG(gpa * gpa) - AVG(gpa) * AVG(gpa)) AS sd_gpa
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
    ROUND((p.access_plus - s.mean_acc) / s.sd_acc, 4) AS access_plus_z,
    ROUND((p.bank_barrier - s.mean_bb) / s.sd_bb, 4) AS bank_barrier_z,
    ROUND((p.resilience - s.mean_res) / s.sd_res, 4) AS resilience_z,
    ROUND((p.motivation - s.mean_mot) / s.sd_mot, 4) AS motivation_z,
    ROUND((p.gpa - s.mean_gpa) / s.sd_gpa, 4) AS gpa_z,
    ROUND(p.access_plus - s.mean_acc, 4) AS access_plus_centered,
    ROUND(p.bank_barrier - s.mean_bb, 4) AS bank_barrier_centered,
    ROUND(p.resilience - s.mean_res, 4) AS resilience_centered,
    ROUND(p.motivation - s.mean_mot, 4) AS motivation_centered,
    CASE
        WHEN p.access_plus > 4.00 THEN 'High_Access'
        ELSE 'Low_Access'
    END AS access_tier
FROM research_participants p
CROSS JOIN stats s;

-- View 2: Aggregated Group Metrics across Access Tiers
CREATE VIEW v_access_tier_summary AS
SELECT
    access_tier,
    COUNT(*) AS n,
    ROUND(AVG(gpa), 2) AS mean_gpa,
    ROUND(AVG(resilience), 2) AS mean_resilience,
    ROUND(AVG(motivation), 2) AS mean_motivation,
    ROUND(AVG(bank_barrier), 2) AS mean_bank_barrier
FROM v_participant_standardized
GROUP BY access_tier;

-- View 3: Resilience Tertiles for Interaction Diagnostics
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
