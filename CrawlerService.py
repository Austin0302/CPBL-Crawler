import DataProvider
import DataTransformer
import Match
from GameStatus import GameStatus
from TCZB import Logger, LogLevel, Globals,Datetime,String
from datetime import datetime, timedelta
from pytz import timezone
import time

class CrawlerService(object):
    def __init__(self, logger, gameType, source, realTime=False, timeOffset=None, machineName=None):
        self.logger = logger
        self.provider = DataProvider.DataProvider(self.logger)
        self.transformer = DataTransformer.DataTransformer(self.logger)
        self.gameType = gameType 
        self.source = source  
        self.realTime = realTime 
        self.timeOffset = timeOffset       
        self.matchCache = {}              
        self.machineName = machineName 
        self.lastLogTime = Datetime.Now()

    def GetMatch(self,date=None):      
        data = self.provider.GetGameData()
        # changedMatch = []
        # print('hi')
        # print(html)
        # eastern = timezone('US/Eastern')
        # # 時間前後一天
        # if self.timeOffset is not None:
        #     timeOffSet = Datetime.Now(eastern).date() + timedelta(days=self.timeOffset)
        #     date = str(timeOffSet)

        # if date is None:
        #     date = str (Datetime.Now().date())
                    
        # if self.realTime == True:
        #     self.parserStartTime(eastern,date)
        # html =  self.provider.GetGameID(date)
        # if html ==None:
        #     return changedMatch
        # gameids =  self.transformer.FilterGameID(html)
        # if gameids == []:
        #     return  changedMatch
        # gameids =   self.serchGameid(date,gameids)
        # if gameids is None:
        #     return changedMatch
        # for i in range(len (gameids)):
        #     gameid = gameids[i]
        #     gameData =  self.provider.GetGameData(gameid)
        #     match =  self.transformer.FilterGameData(gameData,gameid)
        #     if match == []:
        #         return changedMatch
        #     if match.gameID in self.matchCache and match.Equal(self.matchCache[match.gameID]):
        #         return changedMatch
        #     self.matchCache[match.gameID] = match
        #     changedMatch.append(match.GetMatch())
        
        return changedMatch

    #對應GameID
    def serchGameid(self,date,gameids):
        realtimgamids = []
        for gameid in gameids:
            if date in gameid[0][1]:
                realtimgamids.append(gameid)        
        return realtimgamids



    #根據Config時間啟動
    def parserStartTime(self,eastern,date):
        USTime= int(Datetime.Now(eastern).strftime("%H"))
        while (Globals.Globals.CrawlerData['StartTime'] > USTime or USTime > Globals.Globals.CrawlerData['EndTime']):
            USTime= int(Datetime.Now(eastern).strftime("%H"))            
            self.logger.PostLog(LogLevel.LogLevel.Information.name, "sleeping"+ self.machineName + ", Date: " + str(date))
            time.sleep(60)