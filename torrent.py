import libtorrent as lt
import time
import os
from buzzheavier import upload_to_buzzheavier

DOWNLOAD_DIR = "/tmp/tors"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

ses = lt.session()
ses.listen_on(6881, 6891)

settings = {
    'user_agent': 'libtorrent/2.0',
    'listen_interfaces': '0.0.0.0:6881',
}
ses.apply_settings(settings)

ses.add_dht_router("router.utorrent.com", 6881)
ses.add_dht_router("router.bittorrent.com", 6881)
ses.add_dht_router("dht.transmissionbt.com", 6881)
ses.start_dht()

def download_and_upload(magnet):
    params = {
        'save_path': DOWNLOAD_DIR,
        'storage_mode': lt.storage_mode_t.storage_mode_sparse,
    }

    handle = lt.add_magnet_uri(ses, magnet, params)

    while not handle.has_metadata():
        time.sleep(1)

    while True:
        s = handle.status()
        if s.is_seeding or s.is_finished:
            break
        time.sleep(1)

    links = []
    for f in os.listdir(DOWNLOAD_DIR):
        path = os.path.join(DOWNLOAD_DIR, f)
        if os.path.isfile(path):
            link = upload_to_buzzheavier(path)
            links.append(link)

    return links
