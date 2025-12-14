from flask import Flask, request, jsonify
from torrent import download_and_upload

app = Flask(__name__)

@app.route("/add", methods=["POST"])
def add():
    magnet = request.json.get("magnet")
    if not magnet or not magnet.startswith("magnet:"):
        return jsonify({"error": "Invalid magnet"}), 400

    links = download_and_upload(magnet)

    return jsonify({
        "status": "completed",
        "links": links
    })
