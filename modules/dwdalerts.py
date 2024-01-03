import os, datetime, requests
from dwdwfsapi import DwdWeatherWarningsAPI

WARN_PIC = [0,0,0,63488,63488,0,0,0,0,0,63488,65535,65535,63488,0,0,0,0,63488,0,0,63488,0,0,0,63488,65535,0,0,65535,63488,0,0,63488,65535,65535,65535,65535,63488,0,63488,65535,65535,0,0,65535,65535,63488,63488,65535,65535,65535,65535,65535,65535,63488,63488,63488,63488,63488,63488,63488,63488,63488]

def updateUlanzi(config, text, color):
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
            'data': WARN_PIC,
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
            'scrollText': True,
            'scrollTextDelay': 80,
            'centerText': False,
            'position': {
                'x': 7,
                'y': 1,
            },
            'hexColor': color,
        },
    }
    response = requests.post(uri, headers=headers, json=json_data)
    response.raise_for_status()


LATITUDE = os.getenv("HOME_LATITUDE")
LONGITUDE = os.getenv("HOME_LONGITUDE")
DWD = DwdWeatherWarningsAPI((LATITUDE, LONGITUDE))


def update(config, step):
    minVisLevel = step["vis-min-level"]

    now = datetime.datetime.now(datetime.timezone.utc)
    try:
        if now - DWD.last_update > datetime.timedelta(minutes=15):
            DWD.update()
    except:
        DWD = DwdWeatherWarningsAPI((LATITUDE, LONGITUDE))
        return False
    
    if not DWD.data_valid:
        return False
    
    headlines, color, maxLevel = "", None, -1

    for warning in DWD.expected_warnings:
        if warning["level"] >= minVisLevel:
            headlines += warning["headline"] + " - "
            if warning["level"] > maxLevel:
                color = warning["color"]
                maxLevel = warning["level"]

    for warning in DWD.current_warnings:
        if warning["level"] >= minVisLevel:
            headlines += warning["headline"] + " - "
            if warning["level"] > maxLevel:
                color = warning["color"]
                maxLevel = warning["level"]

    if headlines != "":
        updateUlanzi(config, headlines, color)
        return True
    
    return False



if __name__ == "__main__":
    dwd = DWD
    print(f"Warncell id: {dwd.warncell_id}")
    print(f"Warncell name: {dwd.warncell_name}")
    print(f"Number of current warnings: {len(dwd.current_warnings)}")
    print(f"Current warning level: {dwd.current_warning_level}")
    print(f"Number of expected warnings: {len(dwd.expected_warnings)}")
    print(f"Expected warning level: {dwd.expected_warning_level}")
    print(f"Last update: {dwd.last_update}")
    print('-----------')
    for warning in dwd.current_warnings:
        print(warning)
        print('-----------')
    for warning in dwd.expected_warnings:
        print(warning)
        print('-----------')
