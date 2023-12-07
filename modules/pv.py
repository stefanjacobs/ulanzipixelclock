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


from huawei_solar import HuaweiSolarBridge
import asyncio

async def init():
    from config import Config
    c = Config()
    host = c.get("pv.host")
    port = c.get("pv.port")
    slave_id = c.get("pv.slave_id")
    return await HuaweiSolarBridge.create(host=host, port=port, slave_id=slave_id)

async def getData(bridge):
    return await bridge.update()


loop = asyncio.new_event_loop()
bridge = loop.run_until_complete(init())
currentData = None


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


def update(config, _step):
    global loop, bridge, currentData
    try:
        data = loop.run_until_complete(getData(bridge))
    except Exception as e:
        bridge = loop.run_until_complete(init())
        return False

    currentData = data

    if data["input_power"] == 0:
        return False
    
    value = formatValue(data["input_power"].value)

    updateUlanzi(config, value)
    return True


if __name__ == "__main__":
    data = loop.run_until_complete(getData(bridge))
    loop.run_until_complete(bridge.stop())

    pass