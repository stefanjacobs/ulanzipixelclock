from dotenv import load_dotenv

load_dotenv()

import logging, datetime, pytz
from config import Config
from sleeprange import wait
import modules.clock as clock
import modules.bkw as bkw
import modules.em3 as em3
import modules.trash as trash
import modules.sleep as sleep
import modules.advent as advent
import modules.birthday as birthday
import modules.washing as washing
import modules.pv as pv
import modules.battery as battery
import modules.wallbox as wallbox
import modules.car as car
import modules.sunset as sunset


logging.basicConfig(
    level=logging.INFO,  # Wählen Sie den gewünschten Log-Level aus (DEBUG, INFO, WARNING, ERROR, etc.)
    format='%(asctime)s %(levelname)s: %(message)s',  # Hinzufügen des Zeitstempels
    datefmt='%Y-%m-%d %H:%M:%S'  # Format des Zeitstempels
)
log = logging.getLogger(__name__)


def singlestep(config, step):
    match step["name"]:
        case "bkw":         return bkw.update(config, step)
        case "pv":          return pv.update(config, step)
        case "battery":     return battery.update(config, step)
        case "em3":         return em3.update(config, step)
        case "wallbox":     return wallbox.update(config, step)
        case "car":         return car.update(config, step)
        case "trash":       return trash.update(config, step)
        case "advent":      return advent.update(config)
        case "birthday":    return birthday.update(config)
        case "washing":     return washing.update(config, step)
        case "clock":       return clock.update(config)
        case "sunset":      return sunset.update(config, step)
        case _:
            log.error(
                "Something strange happened, the singlestep failed and no exception was thrown"
            )
            raise Exception(
                "Singlestep failed, none of the above status checks succeeded. Should not happen."
            )


def mainloop(config: Config):
    steps = config.get("show")
    maxSteps = len(steps)
    current = 0
    sleepStart = config.get("uptime.start")
    sleepEnd = config.get("uptime.end")
    sleepInterval = config.get("uptime.sleepinterval")
    tz = pytz.timezone("Europe/Berlin")

    while True:
        now = datetime.datetime.now(tz)
        start = now.replace(hour=sleepStart["hour"], minute=sleepStart["minute"])
        end = now.replace(hour=sleepEnd["hour"], minute=sleepEnd["minute"])
        wake_time = now.replace(
            hour=sleepStart["hour"],
            minute=sleepStart["minute"] + int(sleepInterval / 60),
        )
        try:
            result = False
            if not (start <= now and now <= end): # sleep time for ulanzi
                sleep.sleepUlanzi(config)
                wait(sleepInterval)
                continue

            if start <= now and now <= wake_time: # it is wake up time!
                sleep.wakeUp(config)

            if (sleep.statusUlanziSleeping(config)) == True: # manual sleep at ulanzi case
                log.info("Manual sleeping")
                wait(sleepInterval)
                continue

            log.info("Stepping into " + steps[current]["name"])
            result = singlestep(config, steps[current])
            if result == True:
                wait(config.get("showtime"))
            else:
                log.info("Skipping " + steps[current]["name"])
                pass
        except Exception as e:
            log.error(e)
            log.error("Program is ignoring the previous error and continues.")
        finally:
            current = (current + 1) % maxSteps


if __name__ == "__main__":
    config = Config("cfg/config.yml")
    log.setLevel(config.get("log-level"))
    mainloop(config)
