import requests, json

GREEN = "#32612D"

def updateUlanzi(config, watt):
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
            'data': [ 0, 0, 65504, 0, 0, 65504, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65504, 0, 0, 65504, 65504, 0, 0, 65504, 0, 0, 65504, 65504, 65504, 65504, 0, 0, 0, 0, 65504, 65504, 65504, 65504, 0, 0, 65504, 0, 0, 65504, 65504, 0, 0, 65504, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 65504, 0, 0, 65504, 0, 0, ],
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
            'hexColor': GREEN,
        },
    }
    response = requests.post(uri, headers=headers, json=json_data)
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    return


def getWattReading(step):
    response = requests.get(step["uri"])
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    response = json.loads(response.text)
    return response["switch:0"]["apower"]


def update(config, step):
    currentVal = getWattReading(step)
    if round(currentVal) == 0:
        return False
    currentVal = str(round(currentVal)) + "W"
    updateUlanzi(config, currentVal)
    return True




# if __name__ == "__main__":
#     import config
#     c = config.Config("cfg/config.yml")
#     step = [s for s in c.get["show"] if s["name"] == "bkw"]
#     update(c)