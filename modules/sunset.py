from astral import LocationInfo, zoneinfo
from astral.sun import sun
import datetime, requests, os

SUNSET = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,20800,43680,43680,43680,43680,43680,43680,20800,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,43680,64512,64512,64512,64512,64512,64512,64512,64512,43680,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,43680,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,43680,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,43680,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,43680,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14563,14563,14563,20800,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,20800,14563,14563,14563,0,0,0,0,0,14563,14563,14563,14563,14659,14659,14659,14659,43680,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,64512,43680,14659,14659,14659,14659,14563,14563,14563,14563]

SUNRISE = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,21152,44352,44352,44352,44352,44352,44352,21152,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,44352,65504,65504,65504,65504,65504,65504,65504,65504,44352,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,44352,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,44352,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,44352,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,44352,0,0,0,0,0,0,0,0,0,0,0,0,0,0,14787,14787,14787,21152,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,21152,14787,14787,14787,0,0,0,0,0,14787,14787,14787,14787,16929,16929,16929,16929,44352,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,65504,44352,16929,16929,16929,16929,14787,14787,14787,14787]


def updateUlanzi(config, pic):
    uri = config.get("ulanzi.uri")
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'sleepMode': False,
        'switchAnimation': {
            'aktiv': True,
            'animation': 'random',
        },
        'bitmap': {
            'data': pic,
            'position': {
                'x': 0,
                'y': 0,
            },
            'size': {
                'width': 32,
                'height': 8,
            },
        }
    }
    response = requests.post(uri, headers=headers, json=json_data)
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    return


LATITUDE = os.getenv("HOME_LATITUDE")
LONGITUDE = os.getenv("HOME_LONGITUDE")

CITY = LocationInfo("Berlin", "Germany", "Europe/Berlin", LATITUDE, LONGITUDE)
TIMEZONE = zoneinfo.ZoneInfo("Europe/Berlin")


def update(config, _):
    now = datetime.datetime.now(tz=TIMEZONE)
    sunObserver = sun(CITY.observer, date=datetime.date.today(), tzinfo=TIMEZONE)

    sunrise = sunObserver["sunrise"]
    sunset = sunObserver["sunset"]
    trange = datetime.timedelta(minutes=15)

    if sunset - trange <= now <= sunset + trange:
        updateUlanzi(config, SUNSET)
        return True
    if sunrise - trange <= now <= sunrise + trange:
        updateUlanzi(config, SUNRISE)
        return True
    
    return False
