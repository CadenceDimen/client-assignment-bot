import pandas as pd
import requests
import datetime

# 🔗 Replace this with your real Power BI push URL
PUSH_URL = "YOUR_REAL_PUSH_URL_HERE"

# Load your Team Profiles Excel
team_df = pd.read_excel("Team Profiles.xlsx", sheet_name="Team Data")
team_df.columns = team_df.columns.str.strip()

# Loop through each row using existing columns
for _, row in team_df.iterrows():
    team_name = row['Name']
    starting_count = row.get('Clients_Count', 0)

    if pd.isna(starting_count) or int(starting_count) == 0:
        continue

    for i in range(int(starting_count)):
        data = [{
            "client_name": "Baseline",
            "client_type": "Starting Count",
            "client_tier": "",
            "complexity": "",
            "location": "",
            "language": "",
            "referral_status": "",
            "estimate": 0,
            "unique_factor": "",
            "signed_proposal": "",
            "team": team_name,
            "timestamp": datetime.datetime.now().isoformat()
        }]
        response = requests.post(PUSH_URL, json=data)
        print(f"✅ Pushed {i+1}/{starting_count} for {team_name}")
