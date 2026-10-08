CREATE OR REPLACE VIEW account_kpis AS
SELECT
  COUNT(*) AS reels,
  COALESCE(SUM(plays), 0) AS plays,
  COALESCE(SUM(reach), 0) AS reach,
  COALESCE(SUM(total_engagement), 0) AS engagements,
  COALESCE(SUM(follows), 0) AS follows,
  ROUND(SUM(total_engagement) / NULLIF(SUM(reach), 0), 4) AS engagement_rate,
  ROUND(SUM(follows) / NULLIF(SUM(reach), 0), 4) AS follow_conversion_rate,
  ROUND(AVG(completion_rate), 4) AS avg_completion_rate
FROM fact_reels;
