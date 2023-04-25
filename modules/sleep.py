import requests, json

def sleepUlanzi(config):    
    uri = config.get("ulanzi.uri")
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        "sleepMode": True
    }
    response = requests.post(uri, headers=headers, json=json_data)
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    return


def statusUlanziSleeping(config):
    uri = config.get("ulanzi.info")
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.get(uri, headers=headers)
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    response = json.loads(response.text)
    return response["sleepMode"]


def wakeUp(config):
    uri = config.get("ulanzi.uri")
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        "sleepMode": False
    }
    response = requests.post(uri, headers=headers, json=json_data)
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    return

