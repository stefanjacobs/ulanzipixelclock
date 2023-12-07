import requests, pv

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
            'data': [0,0,65535,65535,65535,65535,0,0,0,0,65535,2016,2016,65535,0,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,2016,2016,2016,2016,65535,0,0,65535,65535,65535,65535,65535,65535,0],
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

    currentData = pv.currentData

    showSOC = str(currentData["storage_state_of_capacity"].value) + currentData["storage_state_of_capacity"].unit

    # chargeDischarge scheint Positiv Batterie laden zu sein, negativ entladen
    chargeDischarge = currentData["storage_charge_discharge_power"].value
    
    if currentData["storage_state_of_capacity"].value >= 80.0 and chargeDischarge == 0:
        return False
    
    if currentData["storage_state_of_capacity"].value <= 5.0 and chargeDischarge == 0:
        return False
    
    _, color = formatValue(chargeDischarge)
    
    updateUlanzi(config, showSOC, color)
    return True
    
    # zeige batterie daten an:
    # orange %-Zahl bei discharge oder <20% soc
    # bei discharge oder 0 und <= 5% --> skip
    # grüne %-Zahl bei charge 
    # bei charge oder 0 und >= 80% --> skip

