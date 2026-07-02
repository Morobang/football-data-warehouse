-- EDA — Premier League, scoped first before expanding to all leagues
-- Queries against workspace.gold.fact_matches

-- Home advantage over time
SELECT season,
       AVG(CASE WHEN result = 'H' THEN 1.0 ELSE 0.0 END) AS home_win_rate
FROM workspace.gold.fact_matches
WHERE league = 'E0'
GROUP BY season
ORDER BY season;
