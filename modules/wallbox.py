import requests, json


GREEN = "#32612D"


def updateUlanzi(config, power):
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
            'data': [0,0,0,0,0,0,65504,0,0,0,0,0,0,65504,65504,65504,63488,63488,63488,0,0,0,65504,0,63488,45055,45055,63488,0,0,0,0,63488,45055,45055,45055,63488,63488,63488,0,63488,63488,63488,63488,63488,63488,63488,0,43008,43008,43008,54970,44373,43008,43008,0,0,0,0,44373,54970,0,0,0],
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
            'textString': power,
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
    response.raise_for_status()


def getWattReading(step):
    response = requests.get(step["evcc-uri"])
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    response = json.loads(response.text)
    return response

def formatValue(val):
    val = round(val)
    # check, if W or kW
    einheit = "W"
    if abs(val) > 999:
        val = round(val/1000, 1)
        einheit = "kW"

    # format watt string
    value = str(val) + einheit
    return value

def update(config, step):
    reading = getWattReading(step)
    chargePower = reading["loadpoints"][0]["chargePower"]

    if chargePower == 0:
        return False
    chargePower = formatValue(chargePower)
    updateUlanzi(config, chargePower)
    return True

