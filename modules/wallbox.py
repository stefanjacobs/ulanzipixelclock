import requests, json


GREEN = "#32612D"
ORANGE = "#ff781f"


def updateUlanzi(config, watt, color):
    uri = config.get("ulanzi.uri")
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'sleepMode': False,
        'switchAnimation': {
            'aktiv': True,
            'animation': 'fade',
        },
        'bitmap': {
            'data': [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63488,63488,63488,0,0,0,0,0,63488,45055,45055,63488,0,0,0,0,63488,45055,45055,45055,63488,63488,63488,0,63488,63488,63488,63488,63488,63488,63488,0,43008,43008,43008,54970,44373,43008,43008,0,0,0,0,44373,54970,0,0,0],
            'position': {
                'x': 0,
                'y': 0,
            },
            'size': {
                'width': 8,
                'height': 8,
            },
        },
        'text': {
            'textString': watt,
            'bigFont': False,
            'scrollText': False,
            'scrollTextDelay': 0,
            'centerText': True,
            'position': {
                'x': 7,
                'y': 1,
            },
            'hexColor': color,
        },
    }
    response = requests.post(uri, headers=headers, json=json_data)
    response.raise_for_status()


def getWattReading(step):
    response = requests.get(step["evcc-uri"])
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    response = json.loads(response.text)
    return response["total_power"]

def update(config, step):
    return False