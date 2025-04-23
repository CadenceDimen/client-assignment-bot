import requests
import datetime

url = "https://api.powerbi.com/beta/2cca6d2f-748f-4cfb-a5f8-74ee10be33eb/datasets/642256f8-a0a3-49bb-bfea-d4e616ef14f5/rows?experience=power-bi&key=9sKo8OqOhWNjs7sH6i20R%2ByuRBo6nSbDwZq8aSkBURvC%2FV90YvLriUEI0ouMGVL3zxFH8XZ3PIgo%2FcSk%2FsxyqA%3D%3D"

data = [{
    "client_type": "Test Client",
    "team": "Team Demo",
    "timestamp": datetime.datetime.now().isoformat()
}]

response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response Text:", response.text)
