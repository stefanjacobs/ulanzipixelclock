import requests


def update(config):
    uri = config.get("ulanzi.uri")
    headers = {
        'Content-Type': 'application/json',
    }
    json_data = {
        'sleepMode': False,
        'clock': {
            'show': True,
            'switchAktiv': True,
            'withSeconds': False,
            'switchSec': 11,
            'drawWeekDays': True,
            'color': {
                'r': 255,
                'g': 255,
                'b': 255,
            },
            'hexColor': '#FFFFFF',
        },
    }
    response = requests.post(uri, headers=headers, json=json_data)
    return True