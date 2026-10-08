"""Create deterministic, fictional source data so the project works out of the box."""

from datetime import datetime, timedelta
from pathlib import Path
from random import Random

import pandas as pd

root = Path(__file__).resolve().parents[1]
output = root / "data" / "raw" / "reels.csv"
rng = Random(42)
topics = ["Tutorial", "Behind the scenes", "Product", "Community", "Trend"]
rows = []
for index in range(48):
    topic = topics[index % len(topics)]
    published_at = datetime(2026, 7, 1, 9, 0) + timedelta(days=index * 2, hours=(index * 3) % 12)
    duration = rng.choice([12, 18, 27, 38, 52, 68])
    reach = rng.randint(1800, 28000) * (2 if topic == "Tutorial" else 1)
    likes = int(reach * rng.uniform(0.025, 0.11))
    saves = int(reach * rng.uniform(0.008, 0.05))
    shares = int(reach * rng.uniform(0.004, 0.025))
    rows.append(
        {
            "reel_id": f"demo_{index + 1:03}",
            "published_at": published_at.isoformat(),
            "caption": f"A fictional {topic.lower()} Reel #{index + 1}",
            "format": "reel",
            "duration_seconds": duration,
            "plays": int(reach * rng.uniform(1.05, 1.8)),
            "reach": reach,
            "likes": likes,
            "comments": int(likes * rng.uniform(0.03, 0.16)),
            "saves": saves,
            "shares": shares,
            "profile_visits": int(reach * rng.uniform(0.008, 0.04)),
            "follows": int(reach * rng.uniform(0.001, 0.012)),
            "avg_watch_seconds": round(duration * rng.uniform(0.38, 0.88), 2),
            "completion_rate": round(rng.uniform(0.18, 0.76), 3),
            "audio_name": "Original audio",
            "topic": topic,
        }
    )
pd.DataFrame(rows).to_csv(output, index=False)
print(f"Created {len(rows)} fictional Reels at {output}")
