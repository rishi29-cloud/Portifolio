CREATE OR REPLACE VIEW fact_reels AS
SELECT
  reel_id,
  published_at,
  caption,
  topic,
  audio_name,
  format,
  duration_seconds,
  plays,
  reach,
  likes,
  comments,
  saves,
  shares,
  profile_visits,
  follows,
  avg_watch_seconds,
  completion_rate,
  CAST(published_at AS DATE) AS published_date,
  DATE_TRUNC('week', published_at) AS published_week,
  EXTRACT('hour' FROM published_at) AS publish_hour,
  CASE
    WHEN duration_seconds < 15 THEN '0–14 sec'
    WHEN duration_seconds < 31 THEN '15–30 sec'
    WHEN duration_seconds < 61 THEN '31–60 sec'
    ELSE '60+ sec'
  END AS duration_bucket,
  likes + comments + saves + shares AS total_engagement,
  ROUND((likes + comments + saves + shares) / NULLIF(reach, 0), 4) AS engagement_rate,
  ROUND(saves / NULLIF(reach, 0), 4) AS save_rate,
  ROUND(shares / NULLIF(reach, 0), 4) AS share_rate,
  ROUND(follows / NULLIF(reach, 0), 4) AS follow_conversion_rate,
  ROUND(avg_watch_seconds / NULLIF(duration_seconds, 0), 4) AS avg_watch_percentage
FROM raw_reels;
