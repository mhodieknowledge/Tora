import requests
import os
import json

def upload_to_buzzheavier(file_path):
    """
    Upload a file to BuzzHeavier storage.
    Returns a dictionary with status and URL/error message.
    """
    if not os.path.exists(file_path):
        return {'status': 'error', 'message': f'File not found: {file_path}'}
    
    file_name = os.path.basename(file_path)
    url = f"https://w.buzzheavier.com/a2cmbadjson1/{file_name}"
    
    headers = {
        'Authorization': 'Bearer GP8CWHRDD9NMD4IWVZRU',
        'Content-Type': 'application/octet-stream',
        'User-Agent': 'Reqable/2.30.3',
    }
    
    try:
        with open(file_path, 'rb') as f:
            file_size = os.path.getsize(file_path)
            headers['Content-Length'] = str(file_size)
            
            response = requests.put(url, data=f, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                file_id = result.get('data', {}).get('id')
                if file_id:
                    download_url = f"https://buzzheavier.com/{file_id}/download"
                    return {
                        'status': 'success',
                        'url': download_url,
                        'id': file_id
                    }
                else:
                    return {'status': 'error', 'message': 'No file ID in response'}
            else:
                return {
                    'status': 'error',
                    'message': f'Server error: {response.status_code}',
                    'details': response.text[:200]
                }
    except Exception as e:
        return {'status': 'error', 'message': f'Upload failed: {str(e)}'}

# Simple test function
if __name__ == '__main__':
    # Test with a dummy file
    test_file = 'test.txt'
    with open(test_file, 'w') as f:
        f.write('Test content for BuzzHeavier')
    
    result = upload_to_buzzheavier(test_file)
    print(json.dumps(result, indent=2))
    os.remove(test_file)
