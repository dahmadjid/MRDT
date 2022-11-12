import requests
import os
import json
from pathlib import Path
import time
from kivy.utils import platform
from os.path import dirname, join
import logging 
from datetime import datetime
from utils import timeSinceGame
#  "2c6cda2a-108f-4f64-a966-6fc335362da0": "CIBAGAYCAEBAUCIDBEJSGJBJGM5FCVDAAIAQGAQUAEBQSGYA+loss+29",
#     "a92f2c20-4272-400e-9e68-1f0336a8f19d": "CIBQCAIACUCAGAACAUDA4BQDBEKSMM2IKRQACAYDBEBQMDQBAEBQSVQ+loss+15",
#     "7999b834-567e-4d85-9fcd-b494cda2dfc9": "CIBQCAIAGICAGAACAUDA4BQDBEKSMM2IKRQACAYDBEBQMDQBAEBQSVQ+loss+36"

class MRDT():
    def __init__(self):

        
        self.puuid = "WA4BW2Znou5klQs0wA6CZ75W1oNcBefwa4oWPdY6Z8--78-o9bQGAufwC_15TYhx2hnmIDr4vxr9lA"
        
        self.history_path = Path("data/history.json")
        self.decks_path = Path("data/decks.json")
        self.api_text_path = Path("data/key.txt")
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([Permission.INTERNET,Permission.WRITE_EXTERNAL_STORAGE])
            from android.storage import primary_external_storage_path
            primary_ext_storage = primary_external_storage_path()
            mrdt_folder = join(primary_ext_storage,'MRDT')
            
            if not os.path.exists(mrdt_folder):
                 os.mkdir(mrdt_folder)
            self.history_path = join(mrdt_folder,'history.json')
            self.decks_path = join(mrdt_folder,"decks.json")
            self.api_text_path = join(mrdt_folder,"key.txt")
        if os.path.exists(str(self.api_text_path)):
            with open(str(self.api_text_path),'r') as f:
                for line in f:
                    self.api_key = line
        else:
            self.api_key = ''            
        self.match_id_list = []
        self.match_id_dict = {}
       
        if os.path.exists(self.history_path):
            
            with open(str(self.history_path),'r') as f:
                try:
                    
                    self.match_dict = json.load(f)
                    for match_id in self.match_dict:
                        self.match_id_dict[match_id] = timeSinceGame(self.match_dict[match_id].split('+')[5],p =1)
                    self.match_id_dict = sorted(self.match_id_dict.items(),key= lambda x: x[1])
                    for match_id in self.match_id_dict:
                        self.match_id_list.append(match_id[0])

                except Exception as e:
                    logging.error(e)
                    self.match_dict = {}
                    self.match_id_list = []
                      
       
        else:    
            self.match_dict = {}

        if os.path.exists(self.decks_path):
            with open(str(self.decks_path),'r') as f:
                try:
                    self.deck_dict = json.load(f)
                    
                except:
                    self.deck_dict = {}
        else: 
            self.deck_dict = {}  
        
        
        self.stats_dict = {}

        #self.deck_dict = {"CIBQEAICCYSQIAYCAEBAUEIGAMERGJBTHJIWEAICAMERWVIA":"Lulu/Taric"}
        
    def updateStats(self):
        logging.error("Updating Stats")
        self.stats_dict = {}
        for match_result in self.match_dict.values():
            
            match_result = match_result.split("+")
            if match_result[2] == '0' or match_result[2] == '1':
                continue
            if match_result[8] == 'AI':
                continue
            deck_code = match_result[0]
            winloss = match_result[1]

            if deck_code in self.stats_dict:
                if winloss == 'win':
                    self.stats_dict[deck_code]["wins"] += 1
                elif winloss == 'loss':
                    self.stats_dict[deck_code]["losses"] += 1    
            else:
                if deck_code in self.deck_dict:
                    deck_name = self.deck_dict[deck_code]
                else:
                    deck_name = "New Deck"    
                if winloss == 'win':    
                    self.stats_dict[deck_code] = {"deck_name" : deck_name, "wins" : 1, "losses":0}
                elif winloss == 'loss':
                    self.stats_dict[deck_code] = {"deck_name" : deck_name, "wins" : 0, "losses":1}    




    def getMatchList(self,label):
        logging.error("Getting History")
        label.text="Getting last 20 matches..."
        match_list_url = f"https://europe.api.riotgames.com/lor/match/v1/matches/by-puuid/{self.puuid}/ids?api_key={self.api_key}"
        self.match_list = [match_id[1:-1] for match_id in requests.get(match_list_url).text[1:-1].split(",")]
        logging.error("last 20 matches get requests done")

    def getMatchResult(self,match_id,i,label):
        time.sleep(0.1)
        label.text='Getting match result...'+str(i+1)
        try:
            result = requests.get(f"https://europe.api.riotgames.com/lor/match/v1/matches/{match_id}?api_key={self.api_key}").json()["info"]
            logging.error(result)
        except KeyError as e:

            return 'error'
            
            
        game_start_time = result['game_start_time_utc'].split('+')[0] if '+' in result['game_start_time_utc'] else result['game_start_time_utc']
        game_type = result["game_type"] #Ranked, Normal, AI, Tutorial, VanillaTrial, Singleton, StandardGauntlet
        
        game_mode = result['game_mode'] #Constructed, Expeditions, Tutorial

        if result["players"][0]["puuid"] == self.puuid:

            deck_id = result["players"][0]['deck_id']
            player_factions = result["players"][0]["factions"]
            
            if len(player_factions) == 2:
                player_factions = player_factions[0].split('_')[1] + '-' + player_factions[1].split('_')[1]
            elif len(player_factions) == 0:
                player_factions = ""
            elif len(player_factions) == 3:
                player_factions = player_factions[0].split('_')[1] + '-' + player_factions[1].split('_')[1]+ '-' + player_factions[2].split('_')[1]
            else:
                player_factions = player_factions[0].split('_')[1]

            if len(result['players']) == 2:
                enemy_deck_code = result["players"][1]['deck_code']
                enemy_factions = result["players"][1]["factions"]
                
                if len(enemy_factions) == 2:
                    enemy_factions = enemy_factions[0].split('_')[1] + '-' + enemy_factions[1].split('_')[1]
                elif len(enemy_factions) == 3:
                    enemy_factions = enemy_factions[0].split('_')[1] + '-' + enemy_factions[1].split('_')[1] + '-' + enemy_factions[2].split('_')[1]
                elif len(enemy_factions) == 0:
                    enemy_factions = ""
                else:
                    enemy_factions = enemy_factions[0].split('_')[1]
            else:
                enemy_deck_code = 'AI'
                enemy_factions = 'AI'
            
            return result["players"][0]['deck_code']+"+"+result["players"][0]['game_outcome']+"+"+str(result["total_turn_count"]) + "+" + game_mode + "+" + game_type + "+" + game_start_time + "+" + player_factions + "+" + enemy_factions+ '+' +enemy_deck_code + '+' + deck_id
        
        else:
            deck_id = result["players"][1]['deck_id']
            player_factions = result["players"][1]["factions"]
            
            if len(player_factions) == 2:
                player_factions = player_factions[0].split('_')[1] + '-' + player_factions[1].split('_')[1]
            elif len(player_factions) == 0:
                    player_factions = ""
            elif len(player_factions) == 3:
                player_factions = player_factions[0].split('_')[1] + '-' + player_factions[1].split('_')[1]+ '-' + player_factions[2].split('_')[1]
            else:
                player_factions = player_factions[0].split('_')[1]
                
            enemy_factions = result["players"][0]["factions"]
            
            if len(enemy_factions) == 2:
                enemy_factions = enemy_factions[0].split('_')[1] + '-' + enemy_factions[1].split('_')[1]
            elif len(enemy_factions) == 0:
                enemy_factions = ""    
            elif len(enemy_factions) == 3:
                enemy_factions = enemy_factions[0].split('_')[1] + '-' + enemy_factions[1].split('_')[1]+ '-' + enemy_factions[2].split('_')[1]
            else:
                enemy_factions = enemy_factions[0].split('_')[1]          
            return result["players"][1]['deck_code']+"+"+result["players"][1]['game_outcome']+"+"+str(result["total_turn_count"]) + "+" + game_mode + "+" + game_type + "+" + game_start_time + "+" + player_factions + "+" + enemy_factions + '+' +result["players"][0]['deck_code'] + '+' + deck_id
           
    def updateHistory(self,label):
        self.match_id_dict = {}
        self.match_id_list = []
        self.getMatchList(label)
        i = 0
        for match_id in self.match_list:
            # if self.getMatchResult(match_id,i,label) == 'Skipped':
            #     continue
            if not match_id in self.match_dict:
                result = self.getMatchResult(match_id,i,label)
                if result == "error":
                    continue
                logging.error(f"Match {i} acquired")
                self.match_dict[match_id] = result
                i+=1
        logging.error("Match History Accquired")
              
        for match_id in self.match_dict:
            self.match_id_dict[match_id] = timeSinceGame(self.match_dict[match_id].split('+')[5],p =1)
        self.match_id_dict = sorted(self.match_id_dict.items(),key= lambda x: x[1])
        for match_id in self.match_id_dict:
            self.match_id_list.append(match_id[0])   
                #self.match_id_list.append(str(timeSinceGame(self.match_dict[match_id].split("+")[5])) + match_id)
        with open(str(self.history_path),"w+") as f:
            json.dump(self.match_dict,f,indent = 4)
        self.updateStats()
        

    def getGameName(self,puuid):
        return requests.get(f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}?api_key={self.api_key}").json()['gameName']


#bc35b78d-1a60-4835-a90b-0c7639bee7dd
#deckcode :{"deck_name":"fiora/tar","wins":5,"loss":"6}
