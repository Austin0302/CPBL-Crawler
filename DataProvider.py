from TCZB import Logger, LogLevel,Globals
import re
from lxml import etree
import requests
import urllib.request as req
class DataProvider(object):
    def __init__(self,logger,date='',gametype='' ): 
        self.logger = logger
        self.urlSetting = Globals.Globals.CrawlerData["urlSetting"]
        self.session = None

    def GetGameData(self):
        try:
            data = {
            "__RequestVerificationToken": "PJs2QDLZ_wumc1s7vj06xBvsWxZnUiv6eBRJDgnOPTiWmp3M_zTGTP1pRH5QzKmzCORkSB8qz1Ru2iyHGZNMrJWh8P01",
            "GameSno": "1",
            "KindCode": "A",
            "Year": "2017",
            "PrevOrNext": "",
            "PresentStatus": "",
            "SelectKindCode": "A",
            "SelectYear": "2017",
            "SelectMonth": "3"           
                
            }
            headers={
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
            "content-length": "224",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
            "cookie": "FSize=M; FSize=M; _ga=GA1.1.1733930905.1625102618; __RequestVerificationToken=d-2QpFjBcfvCoIoCTN2AmMcNp64SJ82qtDwyTTHZ2rZ1me_O4KKolq9BYPteL_ek5zMuP4macCUEEYRWJ2g8daQyY-I1; slb_cookie=!n1CxQU/EoSldl72LYm/tmeFjxMkEeu31/lXv4n/XTbc1IalRQsOi6KPsArFm/J/L1kWlS0EOSq86KdU=; _ga_XVM9WZM59B=GS1.1.1625119289.4.1.1625124808.0",
            "origin": "https://www.cpbl.com.tw",
            "referer": "https://www.cpbl.com.tw/box?year=2017&KindCode=A&gameSno=1",
            "sec-ch-ua": '" Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
            "sec-ch-ua-mobile": "?0",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "x-requested-with": "XMLHttpRequest"

            }
            url = "https://www.cpbl.com.tw/box/getlive"
            r = requests.post(url,data=data,headers=headers,verify=False)
            print(r.text)

            # gametype = self.urlSetting["GameType"]
            # link = self.urlSetting["https://www.cpbl.com.tw/box?year=2017&KindCode=A&gameSno=1"].format(gametype,gameid[0][0],gameid[0][1],gameid[0][1][5:9])
            # req =  self.GetUrlResponse(link).text
            # html = etree.HTML(req)
            return r.text
        
        except Exception as e:
            print("GetGameData", e)
            self.CloseSession()
            self.logger.PostLog(LogLevel.LogLevel.Error.name, "Get GetGameData API Failed, Error: " + str(e) )
            return []
      
    def GetGameID(self,date):
        try:
            gameType = self.urlSetting["GameType"]
            lengueType = self.urlSetting["LengueType"]
            link = self.urlSetting["gameIDurl"].format(date,date,lengueType,gameType)
            req =  self.GetUrlResponse(link).text
            html = etree.HTML(req)
            return html
        except Exception as e:
            self.CloseSession()
            self.logger.PostLog(LogLevel.LogLevel.Error.name, "Get GetGameID API Failed, Error: " + str(e) )
            return None     

    # def getSession(self):
    #     if self.session is None:
    #         self.session = requests.Session()
    #         self.session.headers.update(self.urlSetting['Header'])
    #     return self.session
    
    def CloseSession(self):
        if self.session is not None:
            self.session.close()
            self.session = None
        
    # def GetUrlResponse(self, url):
    #     session = self.getSession()
    #     urlData = session.get(url)
    #     return urlData

# from TCZB import Logger, LogLevel,Globals
# import re
# from lxml import etree
# import requests
# import urllib.request as req
# class DataProvider(object):
#     def __init__(self,logger,date='',gametype='' ): 
#         self.logger = logger
#         self.urlSetting = Globals.Globals.CrawlerData["urlSetting"]
#         self.session = None

#     def GetGameData(self):
        # url = "https://www.ptt.cc/bbs/movie/index.html"
        # request = req.Request(url, headers={
        #     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        #     # "cookie":"FSize=M; FSize=M; _ga=GA1.1.1733930905.1625102618; __RequestVerificationToken=d-2QpFjBcfvCoIoCTN2AmMcNp64SJ82qtDwyTTHZ2rZ1me_O4KKolq9BYPteL_ek5zMuP4macCUEEYRWJ2g8daQyY-I1; slb_cookie=!n1CxQU/EoSldl72LYm/tmeFjxMkEeu31/lXv4n/XTbc1IalRQsOi6KPsArFm/J/L1kWlS0EOSq86KdU=; _ga_XVM9WZM59B=GS1.1.1625119289.4.1.1625122359.0"
        # })
        # with req.urlopen(request) as response:
        #     data = response.read().decode("utf-8")
        # print(data)
