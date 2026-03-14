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
            'data': [65504,65504,65504,0,65504,0,0,0,65504,65504,65504,0,0,0,0,0,65504,65504,65504,0,65504,0,0,43680,0,0,0,0,0,0,43680,65205,65504,0,65504,0,0,43680,65205,65205,0,0,0,0,43680,65205,1055,65205,0,0,0,0,0,65205,65205,65205,0,0,0,0,0,65205,65205,65205],
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
    response.raise_for_status()


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


def getReading(step):
    response = requests.get(step["evcc-uri"])
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    response = json.loads(response.text)
    return response


def getPvPower(data):
    pv_meters = data.get("pv")
    if isinstance(pv_meters, list) and pv_meters:
        valid_meters = [meter for meter in pv_meters if isinstance(meter, dict) and meter.get("power") is not None]
        if valid_meters:
            return max(valid_meters, key=lambda meter: meter["power"])["power"]

    site = data.get("site")
    if isinstance(site, dict):
        pv = site.get("pv")
        if isinstance(pv, dict):
            power = pv.get("power")
            if power is not None:
                return power

    return None


def update(config, step):

    data = getReading(step)
    if data is None:
        return False

    input_power = getPvPower(data)
    if input_power is None:
        return False

    if abs(input_power) < 3:
        return False
    
    value = formatValue(input_power)

    updateUlanzi(config, value)
    return True
