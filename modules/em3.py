import requests, json

GREEN = "#32612D"
ORANGE = "#ff781f"

def updateUlanzi(config, watt, color):
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
            'data': [0,0,0,0,64512,65514,65504,64512,0,0,0,64512,65514,65504,64512,0,0,0,64512,65514,65504,64512,0,0,0,64512,65514,65504,64512,0,0,0,0,0,64512,64512,65514,65504,64512,0,0,0,64512,65514,65504,64512,0,0,0,64512,65514,65504,64512,0,0,0,64512,65514,65514,64512,0,0,0,0],
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
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    return


def getWattReading(step):
    response = requests.get(step["uri"])
    response.raise_for_status()  # Wirft eine Ausnahme für einen Fehler in der HTTP-Antwort
    response = json.loads(response.text)
    return response["total_power"]


def formatValue(val):
    val = round(val)
    # check color of reading
    color = ORANGE
    if val <= 0:
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


def update(config, step):
    currentVal = getWattReading(step)
    if abs(currentVal) < 50:
        return False
    value, color = formatValue(currentVal)
    updateUlanzi(config, value, color)
    return True



# if __name__ == "__main__":
#     import config
#     c = config.Config("cfg/config.yml")
#     step = [s for s in c.get["show"] if s["name"] == "bkw"]
#     update(c)
