import pandas as pd
import requests
import datetime
import time

# 🔗 Update this with your new Power BI push URL (from new dataset)
PUSH_URL = "https://api.powerbi.com/beta/2cca6d2f-748f-4cfb-a5f8-74ee10be33eb/datasets/7e61dd3a-971e-4bca-acbc-da206861cf61/rows?experience=power-bi&clientSideAuth=0&key=Ik4UhTtlgvLZF42HMcwl%2BIr2soqKsBuRkU3pHUJ2%2B0%2B2sUIquf8eU4W6Nun7cXjhTVyxy6%2FhJoUzNGV9Pgl0Mg%3D%3D"

# ✅ Load Excel
team_df = pd.read_excel("Team Profiles - Copy.xlsx", sheet_name="Team Data")
team_df.columns = team_df.columns.str.strip()

# 🔁 Push billing baseline rows per team
for _, row in team_df.iterrows():
    team_name = row['Name']
    starting_billing = row.get('Starting_Billing', 0)
    max_billing = row.get('Max_Billing', 750000)
    billing_row_count = 10  # You can make this higher for smoother visuals

    print(f"{team_name} → Raw value: {starting_billing} | Type: {type(starting_billing)}")


    if pd.isna(starting_billing) or starting_billing == 0:
        print(f"⚠️ Skipping {team_name} (no starting billing)")
        continue

    billing_per_client = starting_billing / billing_row_count

    print(f"\n💸 Pushing billing rows for {team_name} - ${starting_billing:,.0f}")

    for i in range(billing_row_count):
        data = [{
            "client_name": "Baseline",
            "client_type": "Starting Billing",
            "client_tier": "",
            "complexity": "",
            "location": "",
            "language": "",
            "estimate": billing_per_client,
            "unique_factor": "",
            "signed_proposal": "",
            "team": team_name,
            "timestamp": datetime.datetime.now().isoformat(),
            "max_billing": max_billing
        }]

        response = requests.post(PUSH_URL, json=data)

        if response.status_code == 200:
            print(f"✅ Pushed {i+1}/{billing_row_count} for {team_name}")
        else:
            print(f"❌ Error pushing to {team_name}: {response.status_code} - {response.text}")

        time.sleep(0.5)  # Light delay to avoid rate limiting
