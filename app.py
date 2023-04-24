import requests, logging, json, datetime, pytz
from enum import Enum
from config import Config
from sleeprange import wait
import modules.clock as clock
import modules.bkw as bkw
import modules.em3 as em3
import modules.trash as trash
import modules.sleep as sleep


logging.basicConfig()
log = logging.getLogger(__name__)


def singlestep(config, step):
    if step["name"] == "clock":
        return clock.update(config)
    if step["name"] == "em3":
        return em3.update(config, step)
    if step["name"] == "bkw":
        return bkw.update(config, step)
    if step["name"] == "trash":
        return trash.update(config, step)

    log.error("Something strange happened, the singlestep failed and no exception was thrown")
    raise Exception("Singlestep failed, none of the above status checks succeeded. Should not happen.")


def mainloop(config: Config):
    steps = config.get("show")
    maxSteps = len(steps)
    current = 0
    sleepStart = config.get("sleep.start")
    sleepEnd = config.get("sleep.end")
    # Get the timezone object for New York
    tz = pytz.timezone('Europe/Berlin') 

    while (True):
        now = datetime.datetime.now(tz)
        start = now.replace(hour=sleepStart["hour"], minute=sleepStart["minute"])
        end = now.replace(hour=sleepEnd["hour"], minute=sleepEnd["minute"])

        if not (start <= now and now <= end):
            print("Should be sleeping!")
            sleep.sleepUlanzi(config)
            wait(config.get("sleepinterval"))
            continue

        try:
            result = singlestep(config, steps[current])
        except Exception as e:
            log.error(e)
            log.warn("Program is ignoring the error and continues.")
        finally:
            if result == True:
                wait(config.get("showtime"))
            else:
                print("Skipping " + steps[current]["name"])
            current = (current + 1) % maxSteps


if __name__ == "__main__":
    config = Config("cfg/config.yml")
    log.setLevel(config.get("log-level"))
    mainloop(config)