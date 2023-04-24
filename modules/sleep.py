import requests

def sleepUlanzi(config):    
    uri = config.get("ulanzi.uri")
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        "sleepMode": True
    }
    response = requests.post(uri, headers=headers, json=json_data)
