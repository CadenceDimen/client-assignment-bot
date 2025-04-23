import pandas as pd
import requests
import datetime
import time

# 🔗 Replace this with your actual Power BI Push URL
PUSH_URL = "https://api.powerbi.com/beta/2cca6d2f-748f-4cfb-a5f8-74ee10be33eb/datasets/c440f6a6-03b6-4393-b19a-09dc88d921df/rows?experience=power-bi&key=4dwS07nuINW0A9xhA6vJ96XeF6tn7fTKy2zwJcWml5CxdmaxU%2Bhfclxcwhh8oOqqQb3%2FdDXvOR7SgYScRlZI0w%3D%3D"

# ✅ Load the Excel file with team names and client counts
team_df = pd.read_excel("Team Profiles.xlsx", sheet_name="Team Data")
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
            "unique_factor": "",
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
