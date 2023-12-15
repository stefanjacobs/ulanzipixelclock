import requests
import threading, time
from datetime import datetime
# from huawei_solar import HuaweiSolarBridge
import huawei_solar
import asyncio

huawei_solar.WAIT_FOR_CONNECTION_TIMEOUT = 10

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


class BridgeReader(threading.Thread):    
    
    currentData = None
    stopThread = False

    async def initBridge(self):
        from config import Config
        c = Config()
        host = c.get("pv.host")
        port = c.get("pv.port")
        slave_id = c.get("pv.slave_id")
        return await huawei_solar.HuaweiSolarBridge.create(host=host, port=port, slave_id=slave_id)
    
    async def getData(self, bridge):
        return await bridge.update()

    def __init__(self, name):
        super().__init__(name=name)
    
    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        while not self.stopThread:
            formatted_timestamp = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
            try:
                self.bridge = self.loop.run_until_complete(self.initBridge())
                self.currentData = self.loop.run_until_complete(self.getData(self.bridge))
                self.loop.run_until_complete(self.bridge.client.stop())
                timestamp = time.time()
                print(str(formatted_timestamp) + " - Input: " + str(self.currentData["input_power"].value) + " - Battery Charge: " + str(self.currentData["storage_charge_discharge_power"].value)) 

                if self.currentData["input_power"].value == 0 and self.currentData["storage_state_of_capacity"].value == 0:
                    self.loop.run_until_complete(asyncio.sleep(300))
                else:
                    self.loop.run_until_complete(asyncio.sleep(37))
            except Exception as e:
                print(str(formatted_timestamp) + " - Exception while talking to modbus client: " + str(e))


bridgeReader = BridgeReader("BridgeReader")
bridgeReader.start()


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

    data = bridgeReader.currentData
    if data is None:
        return False
    
    input_power = data["input_power"].value

    if input_power == 0:
        return False
    
    value = formatValue(input_power)

    updateUlanzi(config, value)
    return True


# if __name__ == "__main__":
#     data = loop.run_until_complete(getData(bridge))
#     loop.run_until_complete(bridge.stop())

#     pass
