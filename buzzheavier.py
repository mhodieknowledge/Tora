import os
import requests

BUZZ_TOKEN = "GP8CWHRDD9NMD4IWVZRU"

def upload_to_buzzheavier(file_path):
    if not os.path.exists(file_path):
        raise Exception("File not found")

    name = os.path.basename(file_path)
    url = f"https://w.buzzheavier.com/a2cmbadjson1/{name}"

    headers = {
        "Authorization": f"Bearer {BUZZ_TOKEN}",
        "Content-Type": "application/octet-stream",
        "Content-Length": str(os.path.getsize(file_path)),
        "User-Agent": "Reqable/2.30.3"
    }

    with open(file_path, "rb") as f:
        r = requests.put(url, headers=headers, data=f)

    if r.status_code != 200:
        raise Exception(r.text)

    fid = r.json()["data"]["id"]
    return f"https://buzzheavier.com/{fid}/download"
