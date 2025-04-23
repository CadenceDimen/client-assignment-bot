import requests
import datetime

PUSH_URL = "https://api.powerbi.com/beta/2cca6d2f-748f-4cfb-a5f8-74ee10be33eb/datasets/c440f6a6-03b6-4393-b19a-09dc88d921df/rows?experience=power-bi&key=4dwS07nuINW0A9xhA6vJ96XeF6tn7fTKy2zwJcWml5CxdmaxU%2Bhfclxcwhh8oOqqQb3%2FdDXvOR7SgYScRlZI0w%3D%3D"

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
        "timestamp": datetime.datetime.now().isoformat()
    }]

    response = requests.post(PUSH_URL, json=data)

    if response.status_code == 200:
        print("✅ Data pushed to Power BI!")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")
