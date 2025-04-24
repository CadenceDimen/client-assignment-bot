import requests
import datetime

PUSH_URL = "https://api.powerbi.com/beta/2cca6d2f-748f-4cfb-a5f8-74ee10be33eb/datasets/7e61dd3a-971e-4bca-acbc-da206861cf61/rows?experience=power-bi&clientSideAuth=0&key=Ik4UhTtlgvLZF42HMcwl%2BIr2soqKsBuRkU3pHUJ2%2B0%2B2sUIquf8eU4W6Nun7cXjhTVyxy6%2FhJoUzNGV9Pgl0Mg%3D%3D"

def push_to_power_bi(client_name, client_type, client_tier, complexity,
                     location, language, estimate,
                     unique_factor, signed_proposal, team):
    data = [{
        "client_name": client_name,
        "client_type": client_type,
        "client_tier": client_tier,
        "complexity": complexity,
        "location": location,
        "language": language,
        "estimate": estimate,
        "unique_factor": unique_factor,
        "signed_proposal": signed_proposal,
        "team": team,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    }]

    response = requests.post(PUSH_URL, json=data)

    if response.status_code == 200:
        print("✅ Data pushed to Power BI!")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
