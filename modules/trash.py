import ics, datetime, requests


filename = "cfg/abfuhrtermine-2023.ics"
with open(filename, 'r') as file:
    data = file.read()
calendar = ics.Calendar(data)


black = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
trashGrayRed = [0,0,0,0,21162,0,0,0,0,0,0,21162,0,0,0,0,0,0,21162,44373,54970,0,0,0,0,21162,33808,44373,33808,44373,0,0,21162,21162,21162,21162,21162,21162,21162,0,0,44373,21162,63488,63488,21162,44373,0,0,44373,21162,21162,21162,21162,44373,0,0,44373,21162,21162,21162,21162,44373,0]
trashGrayWhite = [0,0,0,0,21162,0,0,0,0,0,0,21162,0,0,0,0,0,0,21162,44373,54970,0,0,0,0,21162,33808,44373,33808,44373,0,0,21162,21162,21162,21162,21162,21162,21162,0,0,44373,21162,65535,65535,21162,44373,0,0,44373,21162,21162,21162,21162,44373,0,0,44373,21162,21162,21162,21162,44373,0]
trashYellow = [0,0,0,0,65504,0,0,0,0,0,0,65504,0,0,0,0,0,0,65504,44373,54970,0,0,0,0,65514,33808,44373,33808,44373,0,0,65504,65504,65504,65504,65504,65504,65504,0,0,44352,65504,65504,65504,65504,44352,0,0,44352,65504,65504,65504,65504,44352,0,0,44352,65504,65504,65504,65504,44352,0]
trashBrown = [0,0,0,0,29351,0,0,0,0,0,0,29351,0,0,0,0,0,0,29351,44373,54970,0,0,0,0,29351,33808,44373,33808,44373,0,0,29351,29351,29351,29351,29351,29351,29351,0,0,35491,29351,29351,29351,29351,35491,0,0,35491,29351,29351,29351,29351,35491,0,0,35491,29351,29351,29351,29351,35491,0]
trashBlue = [0,0,0,0,1119,0,0,0,0,0,0,1119,0,0,0,0,0,0,1119,44373,54970,0,0,0,0,1119,33808,44373,33808,44373,0,0,1119,1119,1119,1119,1119,1119,1119,0,0,31,1119,1119,1119,1119,31,0,0,31,1119,1119,1119,1119,31,0,0,31,1119,1119,1119,1119,31,0]


def updateUlanzi(config, trashes):
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
            'data': trashes,
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


def getTrashTomorrow():
    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    trash = []
    for event in calendar.events:
        if event.begin.date() == tomorrow:
            if "gelb" in event.name.lower():
                trash.append(trashYellow)
            elif "restmülltonne 120" in event.name.lower():
                trash.append(trashGrayWhite)
            elif "restmülltonne" in event.name.lower():
                trash.append(trashGrayRed)
            elif "biotonne" in event.name.lower():
                trash.append(trashBrown)
            elif "papiertonne" in event.name.lower():
                trash.append(trashBlue)
    return trash


def getTrashToday():
    now = datetime.datetime.now()
    today = datetime.date.today()
    trash = []
    if now.time() > datetime.time(hour=12, minute=00):
        return trash
    for event in calendar.events:
        if event.begin.date() == today:
            if "gelb" in event.name.lower():
                trash.append(trashYellow)
            elif "restmülltonne 120" in event.name.lower():
                trash.append(trashGrayWhite)
            elif "restmülltonne" in event.name.lower():
                trash.append(trashGrayRed)
            elif "biotonne" in event.name.lower():
                trash.append(trashBrown)
            elif "papiertonne" in event.name.lower():
                trash.append(trashBlue)
    return trash


def mergePics(pics):
    result = []
    for i in range(8):
        for t in pics:
            for x in range(i*8, (i+1)*8):
                result.append(t[x])
    return result


def update(config, step):
    trashToday = getTrashToday()
    countToday = len(trashToday)
    trashTomorrow = getTrashTomorrow()
    countTomorrow = len(trashTomorrow)
    if countToday == 0 and countTomorrow == 0:
        return False
    
    countBlack = 4 - countToday - countTomorrow

    trash = []
    for t in trashToday:
        trash.append(t)
    for _ in range(countBlack):
        trash.append(black)
    for t in trashTomorrow:
        trash.append(t)

    trash = mergePics(trash)
    updateUlanzi(config, trash)
    return True

