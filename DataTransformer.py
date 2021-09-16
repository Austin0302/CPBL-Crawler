import Match
from GameStatus import GameStatus
from TCZB import LogLevel, Logger, Globals
import re
import json
class DataTransformer(object):
    def __init__(self,logger): 
        self.logger = logger
        self.playMode = Globals.Globals.CrawlerData["playMode"]
        self.urlTag = Globals.Globals.CrawlerData["urlTag"]

    def FilterGameData(self, html, gameid):
        try:
            gameID = "".join(re.findall(r'\d+',str (gameid[0][0])))
            gameDate = "".join(re.findall(r'\d+-\d+-\d+',str (gameid[0][1])))
            doubleHeader = "N" if "".join(gameid[1]) == "" else "Y"
            for gameModeTag in html.xpath(".//select[@class='box_select select_long']"):
                allStatus = gameModeTag.xpath(".//option[@selected]")[0].xpath("@value")[0]
                gameMode = self.playMode[allStatus]

            homeTeam, awayTeam = html.xpath(self.urlTag["teamTag"])

            homeScore, awayScore = html.xpath(self.urlTag["score"])[0].replace(" ","").split(":")
            boxscore = html.xpath(self.urlTag["boxscore"])[1]
            scoreTag = boxscore.xpath(self.urlTag["scoreTag"])
            teamScore = [i.replace("\xa0","0") for i in scoreTag]
            homeTeamScore = [int(x) for x in teamScore[0:int(len(teamScore)/2)]]
            awayTeamScore = [int(x) for x in teamScore[int(len(teamScore)/2):]]
            scores = list(map(list, list(zip(homeTeamScore, awayTeamScore))))   
            
            scorePath = self.urlTag["scorePath"].format(gameID)
            gameStatus = "".join(html.xpath(scorePath))

            playByPlay=''
            if '局' in gameStatus :
                playByPlay={}
                playByPlay['playingPeriod'] = gameStatus
                playByPlay = json.dumps(playByPlay)
                gameStatus = GameStatus.InProgress.value 
            elif 'VS' in gameStatus :
                gameStatus = GameStatus.Scheduled.value
            elif 'F' in gameStatus:
                gameStatus = GameStatus.Final.value
            elif gameStatus == '2' :
                scores = []
            else: 
                gameStatus == GameStatus.InProgress.value 

            return Match.Match(
                league="cpbl", leagueID="cpbl.com", homeTeam=homeTeam, awayTeam=awayTeam, awayID=awayTeam, gameDate=gameDate, homeID= homeTeam, playByPlay=str(playByPlay),
                gameID=gameID, gameStatus=gameStatus, doubleHeader=doubleHeader, homeScore=homeScore, awayScore=awayScore, scores=scores, gameMode=gameMode
                )
        except Exception as e:
            self.logger.PostLog(LogLevel.LogLevel.Error.name, "FilterGameData API Failed, Error: " + str(e) )
            return []
            
    def FilterGameID(self,html):
        try:
            gameids=[]
            gameid=[]
            doubleHeader=[]
            gametag=html.xpath('//div[@class="one_block"]')
            for game in gametag:
                gametag=game.xpath('.//@onclick')
                gameid.append(re.findall(r'game_id=\d+',str(gametag))+re.findall(r'date=\d+-\d+-\d+',str(gametag)))
                doubleHeader.append("".join(game.xpath('.//th[@width="50"][2]/text()')))
            targetnums = list(zip(gameid,doubleHeader))
            for targetnum in targetnums:
                if targetnum[0] != [] :
                    gameids.append(targetnum)
            return gameids
        except Exception as e:
            self.logger.PostLog(LogLevel.LogLevel.Error.name, "FilterGameID API Failed, Error: " + str(e) )
            return []

    
