-- ==============================================================================
-- Title: Netflix Auto-Play Experiment: Multi-Metric Funnel & Tension Analysis
-- Dialect: MySQL
-- ==============================================================================

WITH SessionMetrics AS (
    -- 1. Calculate raw session-level aggregates per group
    SELECT 
        test_group,
        COUNT(user_id) AS total_sessions,
        SUM(is_bounce) AS total_bounces,
        SUM(clicked_play) AS total_plays,
        SUM(total_watch_time_mins) AS total_watch_mins
    FROM netflix_ab_test_logs
    GROUP BY test_group
)
-- 2. Compute ratios, conversion rates, and engagement averages
SELECT 
    test_group,
    total_sessions,
    
    -- Top of Funnel: Friction Metric (Bounce Rate)
    total_bounces,
    ROUND((total_bounces * 1.0 / total_sessions) * 100, 2) AS bounce_rate_pct,
    
    -- Middle of Funnel: Conversion Metric (Play Rate)
    total_plays,
    ROUND((total_plays * 1.0 / total_sessions) * 100, 2) AS play_conversion_rate_pct,
    
    -- Bottom of Funnel: Engagement Metric (Avg Watch Time)
    ROUND(total_watch_mins, 2) AS total_retention_mins,
    ROUND((total_watch_mins / total_sessions), 2) AS avg_watch_time_per_session_mins
FROM SessionMetrics;