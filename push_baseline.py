import pandas as pd
import requests
import datetime
import time

# 🔗 Replace this with your actual Power BI Push URL
PUSH_URL = "https://api.powerbi.com/beta/2cca6d2f-748f-4cfb-a5f8-74ee10be33eb/datasets/7e61dd3a-971e-4bca-acbc-da206861cf61/rows?experience=power-bi&clientSideAuth=0&key=Ik4UhTtlgvLZF42HMcwl%2BIr2soqKsBuRkU3pHUJ2%2B0%2B2sUIquf8eU4W6Nun7cXjhTVyxy6%2FhJoUzNGV9Pgl0Mg%3D%3D"

# ✅ Load the Excel file with team names and client counts
team_df = pd.read_excel("Team Profiles - Copy.xlsx", sheet_name="Team Data")
team_df.columns = team_df.columns.str.strip()

# 🧾 Show which teams are being loaded and their counts
print("\n📋 Loaded teams and client counts:")
print(team_df[['Name', 'Clients_Count']])

# 🔁 Loop through each row to push starting client records
for _, row in team_df.iterrows():
    team_name = row['Name']
    starting_count = row.get('Clients_Count', 0)

    if pd.isna(starting_count) or int(starting_count) == 0:
        print(f"⚠️ Skipping {team_name} (no Clients_Count)")
        continue

    print(f"\n🔁 Preparing to push {int(starting_count)} baseline rows for team: {team_name}")

    for i in range(int(starting_count)):
        data = [{
            "client_name": "Baseline",
            "client_type": "Starting Count",
            "client_tier": "",
            "complexity": "",
            "location": "",
            "language": "",
            #"referral_status": "",
            "estimate": 0,
            #"unique_factor": "",
            "signed_proposal": "",
            "team": team_name,
            "timestamp": datetime.datetime.now().isoformat()
        }]
        response = requests.post(PUSH_URL, json=data)

        if response.status_code == 200:
            print(f"✅ Pushed {i+1}/{starting_count} for {team_name}")
        else:
            print(f"❌ Error pushing to {team_name}: {response.status_code} - {response.text}")

        time.sleep(0.5)