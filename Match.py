from datetime import datetime

# Match Object that stores Info about each match
class Match(object):
    def __init__(self, league="", leagueID="", homeID="-1", awayID="-1", homeTeam="", awayTeam="", gameDate="", gameTime="12:00",
                 gameID="", playingPeriod="", scores=[], gameMode="", gameStatus="", doubleHeader="N", playByPlay="",homeScore='0',awayScore='0',crawler_mode=''):
        self.league = league
        self.leagueID = leagueID
        self.homeID = homeID
        self.awayID = awayID
        self.homeTeam  = homeTeam
        self.awayTeam  = awayTeam
        self.gameDate = gameDate
        self.gameTime = gameTime
        self.gameID = gameID +"-"+ self.gameDate
        self.homeScore = homeScore
        self.awayScore = awayScore
        self.playingPeriod = playingPeriod
        self.playByPlay = playByPlay
        self.scores = scores
        self.gameMode = gameMode
        self.gameStatus = gameStatus
        self.crawler_mode=crawler_mode
        self.doubleHeader = doubleHeader

    # Sets game_date and game_time by datetime
    def SetTime(self, time=None):
        if time is not None and type(time) is datetime:
            self.gameDate = str(time.date())
            self.gameTime = time.strftime("%H:%M")
    # Return Formated Data
    def GetMatch(self):
        return {
            "league": self.league,
            "league_id": self.leagueID,
            "team_home": self.homeTeam,
            "team_away": self.awayTeam,
            "team_home_id": self.homeID,
            "team_away_id": self.awayID,
            "game_date": self.gameDate,
            "game_time": self.gameTime,
            "game_id": self.gameID,
            "score_home": self.homeScore,
            "score_away": self.awayScore,
            "scores": self.scores,
            "game_mode": self.gameMode,
            "game_status": self.gameStatus,
            "doubleheader": self.doubleHeader,
            "playbyplay": self.playByPlay,
            "crawler_mode":self.crawler_mode
        }

    # Compares self to another match
    def Equal(self, match):
        return (self.league == match.league and \
            self.leagueID == match.leagueID and \
            self.homeTeam == match.homeTeam and \
            self.homeID == match.homeID and \
            self.awayTeam == match.awayTeam and \
            self.awayID == match.awayID and \
            self.gameDate == match.gameDate and \
            self.gameTime == match.gameTime and \
            self.gameID == match.gameID and \
            self.homeScore == match.homeScore and \
            self.awayScore == match.awayScore and \
            self.playingPeriod == match.playingPeriod and \
            self.playByPlay == match.playByPlay and \
            self.scores == match.scores and \
            self.gameMode == match.gameMode and \
            self.gameStatus == match.gameStatus and \
            self.doubleHeader == match.doubleHeader and \
            self.crawler_mode == match.crawler_mode)
