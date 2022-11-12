import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from functools import partial
from MRDT import MRDT
from kivy.uix.screenmanager import ScreenManager, Screen,FadeTransition,NoTransition
import threading
from kivy.utils import platform
from os.path import dirname, join
import os
import logging
from kivy.uix.popup import Popup
from utils import timeSinceGame
import time
from kivy.core.clipboard import Clipboard
from plyer import notification
from kivy.uix.textinput import TextInput
import json
from kivy.clock import Clock


#TODO: Fix bubble for copy/paste in add deck,
# test app in different resolutions and see if u need to change the grid ui system 
#try to find a way fix storage permission crash
Window.clearcolor = hex("#dddddd")
if not platform =='android':
    Window.size = (360,640)


font = 'FrizQuadrataTT.ttf' 
icon_dict ={'Demacia':'icon-demacia.png', 'ShadowIsles':'icon-shadowisles.png', 'Ionia':'icon-ionia.png', 'Freljord':'icon-freljord.png', 'MtTargon':'icon-targon.png', 'Piltover':'icon-piltoverzaun.png', 'Bilgewater':'icon-bilgewater.png', 'Noxus':'icon-noxus.png'}
class Widgets():
    def __init__(self):
        self.tab_list = [] 
        self.log = ''
        self.k =1
        self.time_list = []
widgets = Widgets()

def runMRDT(dt):
    top = topWidget()
    
    sm = ScreenManager(size_hint=(1, 0.855),pos_hint={'x':0, 'y':0.085},transition=NoTransition())
    tabs = tabsWidget(sm)
    global mrdt 
    mrdt = MRDT()
    history = historyScreen()
    winrate = winrateScreen()

    
    sm.add_widget(history)
    sm.add_widget(winrate)
    root_flt.add_widget(top)
    root_flt.add_widget(sm)
    root_flt.add_widget(tabs)
def updateTimeLabels(dt):
    ij = 0
    for time_label in widgets.time_list:
        match_id = mrdt.match_id_list[ij]
        match_result = mrdt.match_dict[match_id].split("+")
        game_start_time = match_result[5]
        time_label.text = timeSinceGame(game_start_time)+" Ago"
        ij=+1
Clock.schedule_once(runMRDT,.5)






def copyCode(instance,deck_code=''):
    Clipboard.copy(deck_code)
    if platform == 'android':
        notification.notify(message='Copied Deck Code', toast=True)
def errorPopup(title,content):
    widgets.label = Label(text=content)
    popup = Popup(title=title, content=widgets.label,
              size_hint=(0.5,0.2),auto_dismiss=False)
    
    return popup
def changeAPIKey(instance):
    def confirm(instance):
        mrdt.api_key = api_key_input.text
        with open(str(mrdt.api_text_path),'w+') as f:
            f.write(mrdt.api_key)
        popup.dismiss()    
    api_key_input = TextInput(hint_text='Deck Code',multiline = False)
    api_key_input.text = Clipboard.paste()
    confirm_btn =Button(text='OK', background_normal=''
            ,background_color = hex("#eeeeee"),color = hex("#212121"),font_name = font)
    confirm_btn.bind(on_release = confirm) 
    grid = GridLayout(cols = 1,spacing=0.5)
    grid.add_widget(api_key_input)
    grid.add_widget(confirm_btn)
    popup = Popup(title='Add Deck', content=grid,
              size_hint=(0.5,0.2))
    popup.open()  
def topWidget():
    def updateBtnCallbackThreaded(instance):
        
        def updateBtnCallback(instance):
            popup=errorPopup(title="Loading...",content="Loading History...")
            popup.open()
            instance.disabled = True
            try:
                mrdt.updateHistory(widgets.label)
                time.sleep(.1)
            
                displayHistory(widgets.grid1)
                displayWinrates(widgets.grid2)

                popup.dismiss()
            except Exception as e:
                logging.error
                widgets.label.text = 'Network Error'
                popup.auto_dismiss = True
            #widgets.label.text = str(e)
            instance.disabled = False

        thread = threading.Thread(target=partial(updateBtnCallback,instance))
        thread.daemon = True
        thread.start()
    
    top = FloatLayout(size_hint=(1, 0.05),pos_hint={'x':0, 'y':0.95})
    name_label = Button(text="black Rk shooter",size_hint=(0.7, 1),pos_hint={'x':0, 'y':0},background_normal='',background_disabled_normal='',background_color = hex("#212121"),font_name=font)
    name_label.bind(on_release=changeAPIKey)
    update_btn = Button(text= "Update",size_hint=(0.3, 1),pos_hint={'x':0.7, 'y':0},background_normal='', background_color = hex("#0d47a1"),font_name = font)
    update_btn.bind(on_release = updateBtnCallbackThreaded)
    top.add_widget(name_label)
    top.add_widget(update_btn)
    return top

def tabsWidget(sm):
    def switchScreen(instance,name="History"):
        if name == "History":
            sm.current = "History"
            widgets.tab_list[0].color = hex("#0000ff")
            widgets.tab_list[1].color = hex("#212121")

        elif name == "Winrate":
            sm.current = "Winrate"
            widgets.tab_list[0].color = hex("#212121")
            widgets.tab_list[1].color = hex("#0000ff")

    grid = GridLayout(cols=3,size_hint=(1, 0.075),pos_hint={'x':0, 'y':0})
    names = ["History","Winrate"]
    for name in names:
        tab = Button(text=name,background_normal="",background_down="",background_color = hex("#eeeeee"),color = hex("#212121"))
        tab.bind(on_press = partial(switchScreen,name=name))
        widgets.tab_list.append(tab)
        grid.add_widget(tab)
    widgets.tab_list[0].color = hex("#0000ff") 
    return grid
def displayHistory(grid):
    grid.clear_widgets()
    i= 0
    while i<20*widgets.k:
        if i >= len(mrdt.match_id_list):
            break
        flt2 = FloatLayout(size_hint_y=None,height = Window.height*.2)
       
        match_id = mrdt.match_id_list[i]
        
        match_result = mrdt.match_dict[match_id].split("+")
        
        player_deck_code = match_result[0]#player
        winloss = match_result[1]#player
        turns = match_result[2]
        game_mode = match_result[3]
        game_type = match_result[4]
        game_start_time = match_result[5]
        player_factions = match_result[6]
        enemy_factions = match_result[7]
        enemy_deck_code = match_result[8]
        deck_id = match_result[9] #player
        enemy_factions_string = ''
        player_factions_string = ''
        
        if winloss == 'win':
            winloss_btn_color = hex("#0d47a1")
            winloss_btn_text = "Win"
        elif winloss == 'loss':
            winloss_btn_color = hex("#c62828")
            winloss_btn_text = "Loss"
        
        winloss_btn = Button(text = winloss_btn_text,background_disabled_normal=''
        ,background_color = winloss_btn_color,color = hex("#ffffff"),
        disabled=True,size_hint=(0.15, 1),pos_hint={'x':0, 'y':0},font_name = font)
        you_label = Label(text = "You",color = hex("#000000"),size_hint=(None,0.1),pos_hint={'x':0.33, 'y':0.75},font_name = font)
        enemy_label = Label(text = "Enemy",color = hex("#000000"),size_hint=(None,0.1),pos_hint={'x':0.66, 'y':0.75},font_name = font)
        
        type_label = Label(text = game_type,color = hex("#000000"),size_hint=(None,0.1),pos_hint={'x':0.25, 'y':0.15},font_name = font)
        turn_label = Label(text = "Turns:"+turns,color = hex("#000000"),size_hint=(None,0.1),pos_hint={'x':0.50, 'y':0.15},font_name = font)
        time_label = Label(text = timeSinceGame(game_start_time)+" Ago",color = hex("#000000"),size_hint=(None,0.1),pos_hint={'x':0.75, 'y':0.15},font_name = font)
        #FFD700
        background_player_deck_btn = Button(background_disabled_normal='',disabled=True
        ,background_color = hex("#FF8C00"),color = hex("#ffffff"),size_hint=(.26, .25),pos_hint={'x':0.25, 'y':0.425})
        background_enemy_deck_btn = Button(background_disabled_normal='',disabled=True
        ,background_color = hex("#FF8C00"),color = hex("#ffffff"),size_hint=(.28, .25),pos_hint={'x':0.58, 'y':0.425})

        player_deck_btn = Button(text = 'Deck Code',background_disabled_normal='',background_normal=''
        ,background_color = hex("#0d47a1"),color = hex("#ffffff"),size_hint=(.24, .2),pos_hint={'x':0.26, 'y':0.45},font_name = font)
        player_deck_btn.bind(on_release=partial(copyCode,deck_code=player_deck_code)) 
        enemy_deck_text = 'AI' if enemy_deck_code =='AI' else 'Deck Code'
        enemy_deck_btn = Button(text = enemy_deck_text,background_disabled_normal='',background_normal=''
        ,background_color = hex("#0d47a1"),color = hex("#ffffff"),disabled_color = hex("#ffffff"),size_hint=(0.26, .2),pos_hint={'x':0.59, 'y':0.45},font_name = font)
        if enemy_deck_code != 'AI':
            enemy_deck_btn.bind(on_release=partial(copyCode,deck_code=enemy_deck_code))
        else:
            
            enemy_deck_btn.disabled = True
        btn =Button(background_disabled_normal=''
        ,background_color = hex("#eeeeee"),color = hex("#212121"),disabled=True,size_hint=(1,1),pos_hint={'x':0, 'y':0})

        
        
        # player_factions_label = Label(text = player_factions_string,color = hex("#000000"),size_hint=(None,0.1),pos_hint={'x':0.33, 'y':0.45},font_name = font)
        # enemy_factions_label = Label(text = enemy_factions_string,color = hex("#000000"),size_hint=(None,0.1),pos_hint={'x':0.66, 'y':0.45},font_name = font)
       
        # player_factions_image = Image(source = "imgs/"+player_factions+'.png',size_hint=(.4,.4),pos_hint={'x':0.2, 'y':0.3})
        # enemy_factions_image = Image(source = "imgs/"+enemy_factions+'.png',size_hint=(.4,.4),pos_hint={'x':0.52, 'y':0.3})
        

        # enemy_factions_icons = [icon_dict[faction.split('_')[1]] for faction in enemy_factions]
        # player_factions_icons = [icon_dict[faction.split('_')[1]] for faction in player_factions]
        
        # ret = combineIcons(player_factions_icons,'player'+str(i)+'.png')
        # if ret==1:
        #     flt2.add_widget(Image(source = player_factions_icons[0],size_hint=(0.4,0.4),pos_hint={'x':0.195, 'y':0.33}))
        # elif ret == 2 or ret == 3:
        #     flt2.add_widget(Image(source = 'player'+str(i)+'.png',size_hint=(0.4,0.4),pos_hint={'x':0.195, 'y':0.33}))
        
        # ret = combineIcons(enemy_factions_icons,'enemy'+str(i)+'.png')
        # if ret==1:
        #     flt2.add_widget(Image(source = enemy_factions_icons[0],size_hint=(0.4,0.4),pos_hint={'x':0.52, 'y':0.33}))
        # elif ret == 2 or ret == 3:
        #     flt2.add_widget(Image(source = 'enemy'+str(i)+'.png',size_hint=(0.4,0.4),pos_hint={'x':0.52, 'y':0.33})) 
        # if os.path.exists('player'+str(i)+'.png'):
        #     os.remove('player'+str(i)+'.png')
        # if os.path.exists('enemy'+str(i)+'.png'):
        #     os.remove('enemy'+str(i)+'.png')    
        flt2.add_widget(btn)
        flt2.add_widget(winloss_btn)
        flt2.add_widget(turn_label)
        flt2.add_widget(type_label)
        flt2.add_widget(time_label)
        widgets.time_list.append(time_label)
        flt2.add_widget(you_label)
        #flt2.add_widget(enemy_factions_image)
        #flt2.add_widget(player_factions_image)
        flt2.add_widget(enemy_label)
        flt2.add_widget(background_player_deck_btn)
        flt2.add_widget(player_deck_btn)
        flt2.add_widget(background_enemy_deck_btn)
        flt2.add_widget(enemy_deck_btn)
        grid.add_widget(flt2)
        i+=1
    show_more_btn = Button(text = 'Show more',background_disabled_normal='',background_normal=''
        ,background_color = hex("#0d47a1"),color = hex("#ffffff"),size_hint=(1,None),pos_hint={'x':0, 'y':0},font_name = font,height = Window.height*.1)
    show_more_btn.bind(on_release=showMore)
    widgets.grid1.add_widget(show_more_btn)    
def showMore(instance):
    widgets.k += 1
    displayHistory(widgets.grid1)

def historyScreen():
    history = Screen(name="History")
    flt = FloatLayout()
    widgets.grid1 = GridLayout(cols=1,spacing=2.5, size_hint_y=None)
    widgets.grid1.bind(minimum_height=widgets.grid1.setter('height'))
    scroll = ScrollView(size_hint=(1, 1),pos_hint={'x':0, 'y':0})
    scroll.add_widget(widgets.grid1)
    flt.add_widget(scroll)
    if not len(mrdt.match_id_list) == 0:
        displayHistory(widgets.grid1)
    
    history.add_widget(flt)
    return history
def addDeck(instance):
    
    def confirm(instance):
        if deck_name_input.text != '' and deck_code_input.text != '':
            mrdt.deck_dict[deck_code_input.text] = deck_name_input.text
            with open(str(mrdt.decks_path),'w+') as f:
                json.dump(mrdt.deck_dict,f,indent=0)
            displayWinrates(widgets.grid2)
            popup.dismiss() 
        
                
    def maxInput(instance,value):
        if len(value) > 20:
            instance.text = value[:-1]

    deck_name_input = TextInput(hint_text='Deck Name',multiline = False)
    deck_name_input.bind(text = maxInput)
    deck_code_input = TextInput(hint_text='Deck Code',multiline = False)
    deck_code_input.text = Clipboard.paste()
    confirm_btn =Button(text='OK', background_normal=''
            ,background_color = hex("#eeeeee"),color = hex("#212121"),font_name = font)
    confirm_btn.bind(on_release = confirm)
    grid = GridLayout(cols = 1,spacing=0.5)
    grid.add_widget(deck_name_input)
    grid.add_widget(deck_code_input)
    grid.add_widget(confirm_btn)
    popup = Popup(title='Add Deck', content=grid,
              size_hint=(0.5,0.2))
    popup.open()
    
def displayWinrates(grid):
    def copyOrDeleteDeck(instance,deck_code=''):
        
        def removeDeck(instance,deck_code=deck_code):
            print(deck_code)
            mrdt.deck_dict.pop(deck_code)
            with open(str(mrdt.decks_path),'w+') as f:
                json.dump(mrdt.deck_dict,f,indent=0)
            displayWinrates(widgets.grid2)
            popup.dismiss()
             
        grid = GridLayout(cols = 1,spacing = 1)
        popup = Popup(title='Details', content=grid,
        size_hint=(0.5,0.2))
        
        copy_deck_btn = Button(text='Copy Deck', background_normal=''
            ,background_color = hex("#eeeeee"),color = hex("#212121"),font_name = font,height=popup.height*.33)
        delete_deck_btn = Button(text='Remove Deck', background_normal=''
            ,background_color = hex("#eeeeee"),color = hex("#212121"),font_name = font,height=popup.height*.33)    
        
        copy_deck_btn.bind(on_release =partial(copyCode,deck_code=deck_code))
        delete_deck_btn.bind(on_release =removeDeck)
        grid.add_widget(copy_deck_btn)
        grid.add_widget(delete_deck_btn)

        popup.open()


    grid.clear_widgets()
    mrdt.updateStats()
    btn_created = 0
    for deck_code,data in mrdt.stats_dict.items():
        if deck_code in mrdt.deck_dict:
            deck_name = data['deck_name']
            wins = data['wins']
            losses = data['losses']
            winrate = int(wins/(wins+losses) * 100)
            
            
            
            btn =Button(text=deck_name+"    W:"+str(wins)+'    L:'+str(losses)+'    '+str(winrate)+'%', background_normal=''
            ,background_color = hex("#eeeeee"),color = hex("#212121"),size_hint_y=None,font_name = font,height=Window.height*.1)
            btn.bind(on_release=partial(copyOrDeleteDeck,deck_code=deck_code))
            grid.add_widget(btn)
            btn_created += 1



    add_deck_btn = Button(text = '+',background_disabled_normal='',background_normal=''
        ,background_color = hex("#eeeeee"),color = hex("#212121"),size_hint=(1,None),pos_hint={'x':0, 'y':0},font_name = font,halign='center',height = Window.height*.1)
    if btn_created == 0:
        add_deck_btn.text = 'Press to Add a deck you have played \nwith (at least once) to display its winrate'
        
    add_deck_btn.bind(on_release=addDeck)        
    grid.add_widget(add_deck_btn)
def winrateScreen():
    widgets.grid2 = GridLayout(cols=1,spacing=2.5, size_hint_y=None)
    widgets.grid2.bind(minimum_height=widgets.grid2.setter('height'))
    scroll = ScrollView(size_hint=(1, 1),pos_hint={'x':0, 'y':0})
    scroll.add_widget(widgets.grid2)
    winrate = Screen(name="Winrate")
    flt = FloatLayout()
    flt.add_widget(scroll)
    displayWinrates(widgets.grid2)
    winrate.add_widget(flt)
    return winrate   
def root():
    global root_flt
    root_flt = FloatLayout(size_hint=(0.97,0.98),pos_hint={'x':0.015, 'y':0.01})
    

    return root_flt


class GUI(App):
    def build(self):
        if platform == 'android':
            from android import loadingscreen
            loadingscreen.hide_loading_screen()
        Window.bind(on_keyboard=self.key_input)
        return root()
    def on_pause(self):
        return True
    def key_input(self, window, key, scancode, codepoint, modifier):
        if key == 27:
            return True  # override the default behaviour
        else:           # the key now does nothing
            return False    
GUI().run()  