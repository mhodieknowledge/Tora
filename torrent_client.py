import libtorrent as lt
import time
import os
import hashlib
import tempfile

class TorrentManager:
    def __init__(self):
        self.session = lt.session()
        # Critical: Use random ports for free tier compatibility
        self.session.listen_on(0, 0)
        
        # Apply optimized settings
        settings = self.session.get_settings()
        settings['user_agent'] = 'render-torrent-client/1.0'
        settings['enable_outgoing_utp'] = True
        settings['enable_incoming_utp'] = True
        settings['active_downloads'] = 1  # Limit concurrent downloads
        self.session.apply_settings(settings)
        
        # Add public DHT nodes for peer discovery
        self.session.add_dht_router("router.bittorrent.com", 6881)
        self.session.add_dht_router("dht.transmissionbt.com", 6881)
        self.session.start_dht()
        
        self.torrents = {}  # info_hash -> {'handle': handle, 'save_path': path}
        self.download_dir = tempfile.mkdtemp(prefix="torrent_")
        print(f"Download directory: {self.download_dir}")

    def add_torrent(self, magnet_link):
        try:
            # Generate a unique save path for this download
            info_hash = hashlib.sha1(magnet_link.encode()).hexdigest()[:16]
            save_path = os.path.join(self.download_dir, info_hash)
            os.makedirs(save_path, exist_ok=True)
            
            params = {
                'save_path': save_path,
                'storage_mode': lt.storage_mode_t.storage_mode_sparse,
            }
            
            handle = lt.add_magnet_uri(self.session, magnet_link, params)
            handle.set_sequential_download(True)  # Better for streaming
            
            self.torrents[info_hash] = {
                'handle': handle,
                'save_path': save_path,
                'added_time': time.time()
            }
            return info_hash
        except Exception as e:
            print(f"Error adding torrent: {e}")
            return None

    def get_status(self, info_hash):
        if info_hash not in self.torrents:
            return None
        
        handle = self.torrents[info_hash]['handle']
        if not handle.is_valid():
            return None
        
        status = handle.status()
        file_path = self.torrents[info_hash]['save_path']
        
        # Find the main file (simplified - for single file torrents)
        main_file = status.name if status.name else "downloading..."
        
        return {
            'name': main_file,
            'progress': status.progress * 100,
            'download_rate': status.download_rate,
            'upload_rate': status.upload_rate,
            'num_peers': status.num_peers,
            'state': str(status.state),
            'save_path': os.path.join(file_path, main_file) if status.progress == 1 else file_path,
            'info_hash': info_hash
        }

    def get_all_status(self):
        statuses = {}
        for info_hash in list(self.torrents.keys()):
            status = self.get_status(info_hash)
            if status:
                statuses[info_hash] = status
            else:
                # Clean up invalid handles
                del self.torrents[info_hash]
        return statuses

    def remove_torrent(self, info_hash):
        if info_hash in self.torrents:
            try:
                self.session.remove_torrent(self.torrents[info_hash]['handle'])
            except:
                pass
            # Clean up local files
            import shutil
            try:
                shutil.rmtree(self.torrents[info_hash]['save_path'], ignore_errors=True)
            except:
                pass
            del self.torrents[info_hash]
