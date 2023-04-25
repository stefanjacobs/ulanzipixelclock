import requests

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
            'data': [65504,65504,65504,0,65504,0,0,0,65504,65504,65504,0,0,0,0,0,65504,65504,65504,0,65504,0,0,65535,0,0,0,0,0,0,65535,65535,65504,0,65504,0,0,65535,65535,65535,0,0,0,0,65535,65535,0,65535,0,0,0,0,0,65535,65535,65535,0,0,0,0,0,65535,65535,65535],
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


def update(config, step):
    return False