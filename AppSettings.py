import json
import os
from TCZB import Setting
class AppSettings(Setting.Setting):
    def GetPRD(self):
         return {
            "ProjectName": "CPBLCrawlerAgent",
            "GameType": "BS",
            "Source": "cpbl.com",
            "Environment": "PRD",
            "LoggerConfig": {
                "AppName": "crawleragentcpblofficial",
                "Destination": ["192.168.9.231:9092", "192.168.9.232:9092", "192.168.9.233:9092"]
            },
            "ZookeeperConfig": {
                "Address": "192.168.9.231:2181",
                "Path": "/crawlerservice/cpblofficial"
            },
            "BootstrapServers": {
                "Internal": [["192.168.9.231:9092", "192.168.9.232:9092", "192.168.9.233:9092"], ["192.168.55.81:9092", "192.168.55.82:9092", "192.168.55.83:9092"]],
                "External": [["192.168.9.231:9092", "192.168.9.232:9092", "192.168.9.233:9092"], ["49.213.1.158:29092", "49.213.1.158:29093", "49.213.1.158:29094"]]
            }

        }
    def GetPRE(self):
         return {
            "ProjectName": "CPBLCrawlerAgent",
            "GameType": "BS",
            "Source": "cpbl.com",
            "Environment": "PRE",
            "LoggerConfig": {
                "AppName": "crawleragentcpblofficial",
                "Destination": ["192.168.9.231:9092", "192.168.9.232:9092", "192.168.9.233:9092"]
            },
            "ZookeeperConfig": {
                "Address": "192.168.9.231:2181",
                "Path": "/crawlerservice/cpblofficial"
            },
            "BootstrapServers": {
                "Internal": [["192.168.9.231:9092", "192.168.9.232:9092", "192.168.9.233:9092"], ["192.168.55.81:9092", "192.168.55.82:9092", "192.168.55.83:9092"]],
                "External": [["192.168.9.231:9092", "192.168.9.232:9092", "192.168.9.233:9092"], ["49.213.1.158:29092", "49.213.1.158:29093", "49.213.1.158:29094"]]
            }
        }
    def GetLocal(self):
        return {
            "ProjectName": "CPBLCrawlerAgent",
            "GameType": "BS",
            "Source": "cpbl.com",
            "Environment": "Local",
            "LoggerConfig": {
                "AppName": "crawleragentcpblofficial",
                "Destination": ["192.168.9.231:9092", "192.168.9.232:9092", "192.168.9.233:9092"]
            },
            "ZookeeperConfig": {
                "Address": "192.168.9.231:2181",
                "Path": "/crawlerservice/cpblofficial"
            },
            "BootstrapServers": {
                "Internal": [["192.168.9.231:9092", "192.168.9.232:9092", "192.168.9.233:9092"], ["192.168.55.81:9092", "192.168.55.82:9092", "192.168.55.83:9092"]],
                "External": [["192.168.9.231:9092", "192.168.9.232:9092", "192.168.9.233:9092"], ["49.213.1.158:29092", "49.213.1.158:29093", "49.213.1.158:29094"]]
            },
            "AppSettings": {
                "KafkaConfig": "Internal",
                "urlSetting":{
                    "GameType":"01",
                    "LengueType":"01",           
                    "gameIDurl" : "http://www.cpbl.com.tw/schedule/index/{}.html?&date={}&gameno={}&sfieldsub=&sgameno={}",
                    "gameUrl":"http://www.cpbl.com.tw/games/play_by_play.html?&game_type={}&{}&game_{}&pbyear={}",
                    "Header":{
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
                    }

                },
                "playMode":{
                    "01" : "regular",
                    "02" : "02",
                    "03" : "playoff",
                    "04" : "regular",
                    "05" : "playoff",
                    "06" : "playoff",
                    "07"     : "07",
                    "14" : "14",
                    "20" : "20",
                    "21" : "21",
                    "92" : "92"
                },
                "urlTag":{
                    "gameModeTag":".//select[@class='box_select select_long']",
                    "statusTag":".//option",
                    "status" :".//@selected",
                    "teamTag" :".//td[@class='team']/text()",
                    "score":".//div[@class='t_cell']/span/text()",
                    "boxscore":".//table[@class='score_table']",
                    "scoreTag":".//td[@align='center']/span/text()",
                    "scorePath":"//li[@id='box_team_{}']//span/text()"
                },
                "StartTime":2,
                "EndTime":11
            }
        }

    
