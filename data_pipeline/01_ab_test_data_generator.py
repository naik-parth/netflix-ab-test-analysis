import pandas as pd
import numpy as np
from datetime import datetime, timedelta

print("Initializing Netflix Experimentation Data Pipeline...")

np.random.seed(42)

NUM_SESSIONS = 15000
START_DATE = datetime(2026, 8, 1)

# Assign Users & Groups
user_ids = [f"U-{100000 + i}" for i in range(NUM_SESSIONS)]
groups = np.random.choice(['A (Control)', 'B (Treatment)'], size=NUM_SESSIONS, p=[0.5, 0.5])

# Generate Session Behavior
records = []
for i in range(NUM_SESSIONS):
    user_id = user_ids[i]
    group = groups[i]
    session_date = START_DATE + timedelta(days=np.random.randint(0, 14), hours=np.random.randint(0, 23))
    
    bounced = False
    clicked_play = False
    watch_time_sec = 0
    
    if group == 'A (Control)':
        bounce_prob, conversion_prob, avg_watch = 0.12, 0.55, 2700
    else:
        bounce_prob, conversion_prob, avg_watch = 0.22, 0.68, 3300
    
    if np.random.rand() < bounce_prob:
        bounced = True
        watch_time_sec = np.random.randint(5, 15)
    else:
        if np.random.rand() < conversion_prob:
            clicked_play = True
            watch_time_sec = int(np.random.normal(loc=avg_watch, scale=600))
        else:
            watch_time_sec = np.random.randint(120, 600)
            
    watch_time_sec = max(watch_time_sec, 5)

    records.append({
        'user_id': user_id,
        'session_timestamp': session_date.strftime('%Y-%m-%d %H:%M:%S'),
        'test_group': group,
        'is_bounce': 1 if bounced else 0,
        'clicked_play': 1 if clicked_play else 0,
        'total_watch_time_mins': round(watch_time_sec / 60.0, 2)
    })

df_experiment = pd.DataFrame(records)
df_experiment.to_csv('netflix_ab_test_logs.csv', index=False)

print("Pipeline Complete! 'netflix_ab_test_logs.csv' generated.")