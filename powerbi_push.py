# powerbi_push.py

import requests
import datetime

# REPLACE this with your real Power BI push URL
PUSH_URL = "https://api.powerbi.com/beta/2a144b72-f239-42d4-8c0e-6f0f17c48e33/datasets/24bb7591-834b-4b3f-aab4-eff31d7f3ea0/rows?experience=power-bi&key=%2Foyj3QxBX2j6SVppNmmw4Z2cI7e6t%2BIIY8%2FtbvM5y6us3iYpHjbC4UoqCOKxOnw6C%2BxKj8n5iMKcBbiIPnxpSA%3D%3D"

def push_to_power_bi(client_type, team):
    data = [{
        "client_type": client_type,
        "team": team,
        "timestamp": datetime.datetime.now().isoformat()
    }]

    response = requests.post(PUSH_URL, json=data)

    if response.status_code == 200:
        print("✅ Data pushed to Power BI!")
    else:
        print(f"❌ Error pushing data: {response.status_code} - {response.text}")
