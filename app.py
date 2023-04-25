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
    if step["name"] == "advent":
        return advent.update(config)
    if step["name"] == "birthday":
        return birthday.update(config)

    log.error("Something strange happened, the singlestep failed and no exception was thrown")
    raise Exception("Singlestep failed, none of the above status checks succeeded. Should not happen.")


def mainloop(config: Config):
    steps = config.get("show")
    maxSteps = len(steps)
    current = 0
    sleepStart = config.get("uptime.start")
    sleepEnd = config.get("uptime.end")
    sleepInterval = config.get("uptime.sleepinterval")
    tz = pytz.timezone('Europe/Berlin') 

    while (True):
        now = datetime.datetime.now(tz)
        start = now.replace(hour=sleepStart["hour"], minute=sleepStart["minute"])
        end = now.replace(hour=sleepEnd["hour"], minute=sleepEnd["minute"])
        wake_time = now.replace(hour=sleepStart["hour"], minute=sleepStart["minute"] + int(sleepInterval/60))
        try:
            result = False
            if not (start <= now and now <= end):
                print("Should be sleeping!")
                sleep.sleepUlanzi(config)
                wait(sleepInterval)
                continue
            
            if start <= now and now <= wake_time:
                print("Should wake up when in wake up time")
                sleep.wakeUp(config)
    
            if (sleep.statusUlanziSleeping(config)) == True:
                print("Manual Sleeping")
                wait(sleepInterval)
                continue

            print("Stepping into " + steps[current]["name"])
            result = singlestep(config, steps[current])
            if result == True:
                wait(config.get("showtime"))
            else:
                print("Skipping " + steps[current]["name"])
        except Exception as e:
            log.error(e)
            log.warn("Program is ignoring the error and continues.")
        finally:
            current = (current + 1) % maxSteps


if __name__ == "__main__":
    config = Config("cfg/config.yml")
    log.setLevel(config.get("log-level"))
    mainloop(config)