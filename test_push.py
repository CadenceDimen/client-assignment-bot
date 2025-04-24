import requests
import datetime

url = "https://api.powerbi.com/beta/2cca6d2f-748f-4cfb-a5f8-74ee10be33eb/datasets/7e61dd3a-971e-4bca-acbc-da206861cf61/rows?experience=power-bi&clientSideAuth=0&key=Ik4UhTtlgvLZF42HMcwl%2BIr2soqKsBuRkU3pHUJ2%2B0%2B2sUIquf8eU4W6Nun7cXjhTVyxy6%2FhJoUzNGV9Pgl0Mg%3D%3D"

data = [{
    "client_type": "Test Client",
    "team": "Team Demo",
    "timestamp": datetime.datetime.now().isoformat()
}]

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
