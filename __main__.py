import CrawlerService
import AppSettings
from TCZB import Kafka, ZooKeeper, Logger, LogLevel, Globals, Datetime
import datetime
import socket
import threading
import time
import sys
import pathlib
import json

def SendNewMatches(services, interval, kafkaProducers):
    while True:
        sleep = threading.Thread(target=time.sleep, args=(interval,))
        sleep.start()
        for service in services:
            unixTime = Datetime.UnixNow()
            matches = service.GetMatch()
            if not matches: continue
            result = {
                "gametype": service.gameType,
                "source": service.source,
                "request_time": unixTime,
                "send_time": Datetime.UnixNow(),
                "crawler_mode":"NonRealTime",
                "machine_name": socket.gethostname(),
                "matches": matches
            }
            print (result)
            if service.realTime:
                result.update({'crawler_mode':"RealTime"})
            for kafka in kafkaProducers:
                kafka.Send("gamedata", json.dumps(result))
            logInfo = "Data Was Sent Successfully! Machine Name: {}".format(service.machineName,)
            
            now = Datetime.Now()
            if (now - service.lastLogTime).total_seconds() > 5:
                service.logger.PostLog(LogLevel.LogLevel.Information.name, logInfo)
                service.lastLogTime = now
        sleep.join()

def SendHistoryMatches(service, startDate, endDate, interval, kafkaProducers):
    days = [startDate + datetime.timedelta(days=x) for x in range((endDate-startDate).days + 1)]
    for day in days:
        sleep = threading.Thread(target=time.sleep, args=(interval,))
        sleep.start()
        unixTime = Datetime.UnixNow()
        matches = service.GetMatch(str(day))
        if not matches: continue
        result = {
            "gametype": service.gameType,
            "source": service.source,
            "request_time": unixTime,
            "send_time": Datetime.UnixNow(),
            "crawler_mode":"NonRealTime",
            "machine_name": socket.gethostname(),
            "matches": matches
        }
        for kafka in kafkaProducers:
            kafka.Send("gamedata", json.dumps(result))
        sleep.join()
        print("Finished Fetching: " + str(day))
            
def main():
    if len(sys.argv) < 4: return
    try: 
        ENVIRONMENT = sys.argv[1]
        CRAWLER_TYPE = int(sys.argv[2])
        INTERVAL = int(sys.argv[3])
        if ENVIRONMENT not in ["Local", "PRD", "PRE"] or CRAWLER_TYPE not in [0, 1, 2] or INTERVAL <= 0: return
    except Exception:
        return
    
    APPSETTINGS = AppSettings.AppSettings(ENVIRONMENT).ReadConfig()
    NAME = APPSETTINGS["ProjectName"]
    GAMETYPE = APPSETTINGS["GameType"]
    SOURCE = APPSETTINGS["Source"]
    MACHINE_NAME = socket.gethostname()
    # try:
    #     repo = git.Repo(pathlib.Path(__file__).parent.parent.absolute())
    #     VERSION = repo.head.commit.committed_datetime
    #     repo.__del__()
    # except Exception:

    VERSION = "Unknown"
    
    logger = Logger.Logger(APPSETTINGS["LoggerConfig"]["AppName"], APPSETTINGS["LoggerConfig"]["Destination"])
    logger.PostLog(LogLevel.LogLevel.Information.name, "{} Starts! Time: {}".format(NAME, Datetime.Now()))
    if APPSETTINGS["Environment"] != "Local":
        zooKeeper = ZooKeeper.ZooKeeper(APPSETTINGS["ZookeeperConfig"]["Address"],APPSETTINGS["ZookeeperConfig"]["Path"])
        zooKeeper.Watch()
        logger.PostLog(LogLevel.LogLevel.Information.name, "{} Received ZooKeeper Configurations!".format(NAME))
    else:
        Globals.Globals.CrawlerData = APPSETTINGS["AppSettings"]
        logger.PostLog(LogLevel.LogLevel.Information.name, "{} Received Local Configurations!".format(NAME))
    kafkaPath = Globals.Globals.CrawlerData["KafkaConfig"]
    kafkaProducers = [Kafka.Kafka(logger, True, server) for server in APPSETTINGS["BootstrapServers"][kafkaPath]]
    configInfo = "{} Received All Configurations! Version: {}, Environment: {}, Service Type: {} (0 - Real-Time / 1 - Non-Real-Time), Repeat Interval: Every {} Seconds."
    logger.PostLog(LogLevel.LogLevel.Information.name, configInfo.format(NAME, VERSION, APPSETTINGS["Environment"], CRAWLER_TYPE, INTERVAL))
    
    if CRAWLER_TYPE == 0:
        realTimeService = CrawlerService.CrawlerService(logger, GAMETYPE, SOURCE, True, 0, MACHINE_NAME)
        SendNewMatches([realTimeService], INTERVAL, kafkaProducers)
    elif CRAWLER_TYPE == 1: 
        yesterdayService = CrawlerService.CrawlerService(logger, GAMETYPE, SOURCE, timeOffset=-1, machineName=MACHINE_NAME, )
        tomorrowService = CrawlerService.CrawlerService(logger, GAMETYPE, SOURCE, timeOffset=1, machineName=MACHINE_NAME, )
        SendNewMatches([yesterdayService, tomorrowService], INTERVAL, kafkaProducers)
    else:
        if len(sys.argv) < 6: return
        date = datetime.datetime.strptime(sys.argv[4], '%Y-%m-%d').date()
        endDate = datetime.datetime.strptime(sys.argv[5], '%Y-%m-%d').date()
        if date > endDate:
            logger.PostLog(LogLevel.LogLevel.Error.name, "Error: historyService start date > end date")
            return
        historyService = CrawlerService.CrawlerService(logger, GAMETYPE, SOURCE, machineName=MACHINE_NAME)
        SendHistoryMatches(historyService, date, endDate, INTERVAL, kafkaProducers)

if __name__ == "__main__":
    main()
