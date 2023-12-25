import requests, json


GREEN = "#32612D"
ORANGE = "#ff781f"


FULL_AKKU = [0,0,65535,65535,65535,65535,0,0,0,0,65535,2016,2016,65535,0,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,65535,65535,65535,65535,65535,0]

AKKU_90 = [0,0,65535,65535,65535,65535,0,0,0,0,65535,0,0,65535,0,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,65535,65535,65535,65535,65535,0]

AKKU_70 = [0,0,65535,65535,65535,65535,0,0,0,0,65535,0,0,65535,0,0,0,65535,0,0,0,0,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,65535,65535,65535,65535,65535,0]

AKKU_50 = [0,0,65535,65535,65535,65535,0,0,0,0,65535,0,0,65535,0,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,65535,65535,65535,65535,65535,0]

AKKU_30 = [0,0,65535,65535,65535,65535,0,0,0,0,65535,0,0,65535,0,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,65504,65504,65504,65504,65535,0,0,65535,65504,65504,65504,65504,65535,0,0,65535,65535,65535,65535,65535,65535,0]

AKKU_10 = [0,0,65535,65535,65535,65535,0,0,0,0,65535,0,0,65535,0,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,64512,64512,64512,64512,65535,0,0,65535,65535,65535,65535,65535,65535,0]

AKKU_EMPTY = [0,0,65535,65535,65535,65535,0,0,0,0,65535,0,0,65535,0,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,0,0,0,0,65535,0,0,65535,65535,65535,65535,65535,65535,0]


def updateUlanzi(config, watt, color, pic):
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
            'data': pic,
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


def formatValue(val):
    val = round(val)
    # check color of reading
    color = ORANGE
    if val >= 0:
        color = GREEN
    val = abs(val)
    
    # check, if W or kW
    einheit = "W"
    if abs(val) > 999:
        val = round(val/1000, 1)
        einheit = "kW"

    # format watt string
    value = str(val) + einheit
    return value, color


def getReading(step):
    response = None
    response = requests.get(step["evcc-uri"])
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    response = json.loads(response.text)
    return response


def update(config, step):

    currentData = getReading(step)

    if currentData is None:
        return False

    # chargeDischarge scheint Positiv Batterie laden zu sein, negativ entladen
    chargeDischarge = currentData["result"]["batteryPower"]
    soc = currentData["result"]["batterySoc"]

    if abs(chargeDischarge) < 50:
        return False
    
    if soc >= 85.0 and chargeDischarge == 0:
        return False
    
    if soc <= 15.0 and chargeDischarge == 0:
        return False
    
    pic = FULL_AKKU
    if soc >= 85:
        pic = FULL_AKKU
    elif soc >= 75:
        pic = AKKU_90
    elif soc >= 55:
        pic = AKKU_70
    elif soc >= 35:
        pic = AKKU_50
    elif soc >= 15:
        pic = AKKU_30
    else:
        pic = AKKU_10

    value, color = formatValue(chargeDischarge)
    updateUlanzi(config, value, color, pic)
    return True
    
    # zeige batterie daten an:
    # orange %-Zahl bei discharge oder <20% soc
    # bei discharge oder 0 und <= 5% --> skip
    # grüne %-Zahl bei charge 
    # bei charge oder 0 und >= 80% --> skip

