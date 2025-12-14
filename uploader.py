import os
import requests

BUZZ_TOKEN = "GP8CWHRDD9NMD4IWVZRU"

def upload_to_buzzheavier(file_path):
    if not os.path.exists(file_path):
        raise Exception("File not found")

    filename = os.path.basename(file_path)
    url = f"https://w.buzzheavier.com/a2cmbadjson1/{filename}"

    headers = {
        "Authorization": f"Bearer {BUZZ_TOKEN}",
        "Content-Type": "application/octet-stream",
        "User-Agent": "Reqable/2.30.3",
        "Content-Length": str(os.path.getsize(file_path))
    }

    with open(file_path, "rb") as f:
        response = requests.put(url, headers=headers, data=f)

    if response.status_code != 200:
        raise Exception(f"Upload failed: {response.status_code} {response.text}")

    data = response.json()
    file_id = data["data"]["id"]
    return f"https://buzzheavier.com/{file_id}/download"
