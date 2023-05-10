import requests, json

BLACK = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

WASHING_ACTIVE = [0,54970,54970,54970,54970,54970,54970,0,0,54970,54970,54970,54970,63488,54970,0,0,65535,65535,65535,65535,65535,65535,0,0,65535,54970,33808,33808,54970,65535,0,0,65535,33808,0,0,33808,65535,0,0,65535,33808,1055,1055,33808,65535,0,0,65535,54970,33808,33808,54970,65535,0,0,65535,65535,65535,65535,65535,65535,0]
WASHING_PASSIVE = [0,54970,54970,54970,54970,54970,54970,0,0,54970,54970,54970,54970,34784,54970,0,0,65535,65535,65535,65535,65535,65535,0,0,65535,54970,33808,33808,54970,65535,0,0,65535,33808,0,0,33808,65535,0,0,65535,33808,0,0,33808,65535,0,0,65535,54970,33808,33808,54970,65535,0,0,65535,65535,65535,65535,65535,65535,0]

DRYER_ACTIVE = [0,65535,65535,65535,65535,65535,65535,0,0,65535,40179,40179,40179,63616,65535,0,0,65535,65535,65535,65535,65535,65535,0,0,65535,65535,64853,64853,65535,65535,0,0,65535,64170,64170,64170,43008,65535,0,0,65535,64170,43008,64170,64170,65535,0,0,65535,65535,64853,64853,65535,65535,0,0,65535,65535,65535,65535,65535,65535,0]
DRYER_PASSIVE = [0,65535,65535,65535,65535,65535,65535,0,0,65535,40179,40179,40179,2016,65535,0,0,65535,65535,65535,65535,65535,65535,0,0,65535,65535,54970,54970,65535,65535,0,0,65535,44373,44373,44373,33808,65535,0,0,65535,44373,33808,44373,44373,65535,0,0,65535,65535,54970,54970,65535,65535,0,0,65535,65535,65535,65535,65535,65535,0]


def updateUlanzi(config, washes):
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
            'data': washes,
            'position': {
                'x': 0,
                'y': 0,
            },
            'size': {
                'width': 32,
                'height': 8,
            },
        },
    }
    response = requests.post(uri, headers=headers, json=json_data)
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    return


def getWattReading(step):
    washingResponse = requests.get(step["wash-uri"], timeout=3)
    washingResponse.raise_for_status()
    washingResponse = json.loads(washingResponse.text)
    washingReading = washingResponse["switch:0"]["apower"]

    dryerResponse = requests.get(step["dryer-uri"], timeout=3)
    dryerResponse.raise_for_status()
    dryerResponse = json.loads(dryerResponse.text)
    dryerReading = dryerResponse["switch:0"]["apower"]

    return round(washingReading), round(dryerReading)


def mergePics(pics):
    result = []
    for i in range(8):
        for t in pics:
            for x in range(i*8, (i+1)*8):
                result.append(t[x])
    return result


def update(config, step):
    washing, drying = getWattReading(step)
    powerOffThreshold = step["power-off-threshold"]
    idleThreshold = step["idle-threshold"]

    # if power less than threshold, nothing is going on at the moment. Skip
    if washing <= powerOffThreshold and drying <= powerOffThreshold:
        return False
    
    wash = []
    
    # One of the two devices is active (idle at least):
    if washing > idleThreshold:
        wash.append(WASHING_ACTIVE)
    else:
        wash.append(WASHING_PASSIVE)
    wash.append(BLACK)
    wash.append(BLACK)
    if drying > idleThreshold:
        wash.append(DRYER_ACTIVE)
    else:
        wash.append(DRYER_PASSIVE)

    wash = mergePics(wash)
    updateUlanzi(config, wash)
    return True
