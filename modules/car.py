import requests, os, logging, datetime
from weconnect import weconnect

GREEN = "#32612D"
CAR_PIC = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,63488,63488,63488,0,0,0,0,0,63488,45055,45055,63488,0,0,0,0,63488,45055,45055,45055,63488,63488,63488,0,63488,63488,63488,63488,63488,63488,63488,0,43008,43008,43008,54970,44373,43008,43008,0,0,0,0,44373,54970,0,0,0]


def updateUlanzi(config, text):
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
            'data': CAR_PIC,
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
            'textString': text,
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


VW_USERNAME=os.getenv("VW_USER")
VW_PASSWORD=os.getenv("VW_PASS")
VW_VIN=os.getenv("VW_VIN")

carcounter = 0

LOG = logging.getLogger("weconnect")
LOG.setLevel(logging.ERROR)

weConnect = weconnect.WeConnect(username=VW_USERNAME, password=VW_PASSWORD, updateAfterLogin=False, loginOnInit=True, maxAge=300)
now = datetime.datetime.now(datetime.timezone.utc)
lastUpdate = now - datetime.timedelta(minutes=16)


def update(config, step):

    global carcounter
    carcounter = (carcounter + 1) % 2

    global lastUpdate
    now = datetime.datetime.now(datetime.timezone.utc)

    if now - lastUpdate > datetime.timedelta(minutes=15):
        weConnect.update(updatePictures=False, updateCapabilities=False)
        lastUpdate = datetime.datetime.now(datetime.timezone.utc)

    match carcounter:
        case 0: # show soc
            soc_pct = weConnect.vehicles[VW_VIN].domains["measurements"]["fuelLevelStatus"].currentSOC_pct.value
            updateUlanzi(config, str(soc_pct) + "%")
            return True
        case 1: # show range
            range_km = weConnect.vehicles[VW_VIN].domains["measurements"]["rangeStatus"].electricRange.value
            updateUlanzi(config, str(range_km) + "km")
            return True
        case _:
            return False