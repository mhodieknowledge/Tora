from flask import Flask, render_template, request, jsonify
import threading
import os
import time
from torrent_client import TorrentManager
from uploader import upload_to_buzzheavier

app = Flask(__name__)
manager = TorrentManager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_torrent():
    magnet_link = request.form.get('magnet')
    if not magnet_link or not magnet_link.startswith('magnet:'):
        return jsonify({'error': 'Invalid magnet link'}), 400
    
    # Start download in background thread
    def download_and_upload():
        info_hash = manager.add_torrent(magnet_link)
        if info_hash:
            print(f"Started download for {info_hash}")
            # Monitor and upload on completion
            while True:
                status = manager.get_status(info_hash)
                if not status:
                    break
                if status['progress'] == 100:  # Download complete
                    file_path = status['save_path']
                    if os.path.exists(file_path):
                        print(f"Uploading {file_path} to BuzzHeavier...")
                        result = upload_to_buzzheavier(file_path)
                        # Store result (in a real app, you'd save to a database)
                        print(f"Upload result: {result}")
                    manager.remove_torrent(info_hash)
                    break
                time.sleep(2)
    
    thread = threading.Thread(target=download_and_upload, daemon=True)
    thread.start()
    
    return jsonify({'message': 'Torrent added to queue'}), 202

@app.route('/status')
def get_status():
    all_status = manager.get_all_status()
    return jsonify(all_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
