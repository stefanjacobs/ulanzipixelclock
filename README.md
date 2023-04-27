# Meine magische Pixeluhr

## Idee

Nutzung einer PixelIt Display Anzeige, die per REST ansprechbar ist und Belieferung der Anzeige über einen zentralen Server, bei mir ein Raspberry Pi. Das Skript sammelt auf Basis von REST Endpunkten im WiFi die benötigten Daten live ein und stellt diese darf.

### Links

- [Ulanzi Pixel Clock](https://www.ulanzi.de/products/ulanzi-pixel-smart-uhr-2882?currency=EUR)
- [Angepasste PixelIt Firmware für Ulanzi](https://github.com/aptonline/PixelIt_Ulanzi)
- [Anleitung zum flashen](https://www.bjoerns-techblog.de/2023/03/pixelit-auf-ulanzi-smart-clock/)

## Was wird alles dargestellt?

Rotation im 30 Sekunden Takt der folgenden Screens:

- Uhr (Uhrzeit, Datum) im Wechsel a 10 sekunden
- Wetter für heute nachmittag
- Solarerzeugung BKW jetzt
- Solarerzeugung Haus
- Energieverbrauch im Haus jetzt
- Energiebilanz gesamt
- Müll (wenn morgen Müll abgefahren wird)
  - Müll für heute
  - Müll für morgen

Rahmenbedingungen:

- Im konfigurierbaren Zeitraum wird die Pixelanzeige schlafen gelegt oder auf Knopfdruck

## Beispielbilder

### Aktuelle Leistung Balkonkraftwerk

![Aktuelle Leistung BKW](./docs/pics/bkw.png)

### Aktuelle Leistung Hausverbrauch

Orange ist Verbrauch, Grün ist Einspeisung

![Aktuelle Leistung Haus](./docs/pics/power.png)

### Uhr

![Beispielbild der Pixeluhr](./docs/pics/clock.png)

### Müllanzeige (links heute, rechts morgen)

![Beispielbild der Mülltonne](./docs/pics/trash.png)

