import os
import subprocess
from flask import Flask, request, jsonify
from uploader import upload_to_buzzheavier

DOWNLOAD_DIR = "/tmp/downloads"

app = Flask(__name__)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/add", methods=["POST"])
def add_torrent():
    magnet = request.json.get("magnet")
    if not magnet:
        return jsonify({"error": "Magnet link required"}), 400

    # Download using aria2
    subprocess.run([
        "aria2c",
        "--seed-time=0",
        "--dir", DOWNLOAD_DIR,
        magnet
    ], check=True)

    files = os.listdir(DOWNLOAD_DIR)
    if not files:
        return jsonify({"error": "No files downloaded"}), 500

    results = []
    for f in files:
        path = os.path.join(DOWNLOAD_DIR, f)
        if os.path.isfile(path):
            link = upload_to_buzzheavier(path)
            results.append({
                "file": f,
                "buzzheavier_link": link
            })

    return jsonify({
        "status": "completed",
        "results": results
    })
