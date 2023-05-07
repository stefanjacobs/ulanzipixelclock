# Meine magische Pixeluhr

## Idee

Nutzung einer PixelIt Display Anzeige, die per REST ansprechbar ist und Belieferung der Anzeige über einen zentralen Server, bei mir ein Raspberry Pi. Das Skript sammelt auf Basis von REST Endpunkten im WiFi die benötigten Daten live ein und stellt diese dar.

### Links

- [Ulanzi Pixel Clock](https://www.ulanzi.de/products/ulanzi-pixel-smart-uhr-2882?currency=EUR)
- [Angepasste PixelIt Firmware für Ulanzi](https://github.com/aptonline/PixelIt_Ulanzi)
- [Anleitung zum flashen](https://www.bjoerns-techblog.de/2023/03/pixelit-auf-ulanzi-smart-clock/)

## Was wird alles dargestellt?

Rotation im 30 Sekunden Takt der folgenden Screens:

- Uhr (Uhrzeit, Datum) im Wechsel a 10 sekunden
- Wetter für heute (tbd)
- Solarerzeugung BKW jetzt
- Solarerzeugung Haus (tbd)
- Energieverbrauch im Haus jetzt
- Energiebilanz gesamt (tbd)
- Adventsbilder und Weihnachtsbilder, wenn das zeitlich zutrifft
- Geburtstags und Vater-/Muttertagsbilder, wenn das zeitlich zutrifft
- Müll (wenn morgen Müll abgefahren wird)
  - Müll für heute
  - Müll für morgen

Rahmenbedingungen:

- Im konfigurierbaren Zeitraum wird die Pixelanzeige schlafen gelegt oder auf Knopfdruck

## Beispielbilder

### Aktuelle Leistung Balkonkraftwerk

Sobald keine Leistung erzeugt wird, wird auch nichts angezeigt.

![Aktuelle Leistung BKW](./docs/pics/bkw.png)

### Aktuelle Leistung Hausverbrauch

Orange ist Verbrauch, Grün ist Einspeisung

![Aktuelle Leistung Haus](./docs/pics/power.png)

### Uhr

![Beispielbild der Pixeluhr](./docs/pics/clock.png)

### Müllanzeige (links heute, rechts morgen)

Wenn heute und morgen kein Müll fällig ist, wird nichts angezeigt. Der Müll für heute wird nur bis 12 Uhr angezeigt, danach machts keinen Sinn mehr. Was weg ist, ist weg...

![Beispielbild der Mülltonne](./docs/pics/trash.png)

