import requests, json
from copy import deepcopy


GREEN = "#32612D"
ORANGE = "#ff781f"

AKKU_BLACK = 0
AKKU_GREEN = 2016
AKKU_YELLOW = 65504
AKKU_ORANGE = 64512

FULL_AKKU = [0,0,65535,65535,65535,65535,0,0,0,0,65535,2016,2016,65535,0,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,65535,65535,65535,65535,65535,0]


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
    color = GREEN
    if val >= 0:
        color = ORANGE
    val = abs(val)
    
    # check, if W or kW
    einheit = "W"
    if abs(val) > 999:
        val = round(val/1000, 1)
        einheit = "kW"

    # format watt string
    value = str(val) + einheit
    return value, color


def formatSOC(soc, val):
    val = round(val)
    # check color of reading
    color = GREEN
    if val >= 0:
        color = ORANGE
    
    # format watt string
    soc = str(soc) + "%"
    return soc, color


def getReading(step):
    response = None
    response = requests.get(step["evcc-uri"])
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    response = json.loads(response.text)
    return response

batcounter = 0

def update(config, step):

    global batcounter
    batcounter = (batcounter + 1) % 2

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
    
    pic = deepcopy(FULL_AKKU)

    # we have here 22 dots that can be colored:
    colorcounter = 0
    maxC = int(round(22 - (22/100*soc)))
    for counter, color in enumerate(pic):
        if colorcounter >= maxC:
            break
        if color == AKKU_GREEN:
            pic[counter] = AKKU_BLACK
            colorcounter += 1

    # if the soc is less than X, replace colors away from green
    if soc < 38:
        pic = [AKKU_YELLOW if x==AKKU_GREEN else x for x in pic]
    elif soc < 16:
        pic = [AKKU_ORANGE if x==AKKU_GREEN else x for x in pic]
    
    match batcounter:
        case 0: # show soc
            value, color = formatSOC(soc, chargeDischarge)
            updateUlanzi(config, value, color, pic)
            return True
        case 1: # show current power
            value, color = formatValue(chargeDischarge)
            updateUlanzi(config, value, color, pic)
            return True
        case _:
            pass

    return False

