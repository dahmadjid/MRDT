import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.utils import get_color_from_hex as hex
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image
from functools import partial
from kivy.uix.screenmanager import ScreenManager, Screen,FadeTransition



Window.clearcolor = hex("#000000")
def topWidget():
    top = FloatLayout(size_hint=(1, 0.05),pos_hint={'x':0, 'y':0.95})
    name_label = Button(text="black Rk shooter",size_hint=(0.7, 1),pos_hint={'x':0, 'y':0},background_disabled_normal='',background_color = hex("#393E46"),disabled=True)
    update_btn = Button(text= "Update",size_hint=(0.3, 1),pos_hint={'x':0.7, 'y':0},background_normal='', background_color = hex("#00adb5"))
    top.add_widget(name_label)
    top.add_widget(update_btn)
    return top
def tabsWidget(sm):
    def switchScreen(instance,name="History"):
        if name == "History":
            sm.current = "History"
        elif name == "Winrate":
            sm.current = "Winrate"
        elif name == "Decoder":
            sm.current = "Decoder"
        
    grid = GridLayout(cols=3,size_hint=(1, 0.05),pos_hint={'x':0, 'y':0.898},spacing = 1)
    names = ["History","Winrate","Decoder"]
    for name in names:
        tab = Button(text=name,background_normal="",background_color = hex("#00adb5"))
        tab.bind(on_press = partial(switchScreen,name=name))
        grid.add_widget(tab)
    return grid

def historyScreen():
    history = Screen(name="History")
    flt = FloatLayout()
    grid = GridLayout(cols=1,spacing=1, size_hint_y=None)
    grid.bind(minimum_height=grid.setter('height'))
    scroll = ScrollView(size_hint=(1, 1),pos_hint={'x':0, 'y':0})
    scroll.add_widget(grid)


    for i in range(20):
        string = f"Deck    Win    {i}"
        grid.add_widget(Button(text=string,size_hint_y=None,background_disabled_normal=''
        ,background_color = hex("#222831"),disabled=True,height = 120))
    
    
    flt.add_widget(scroll)
    history.add_widget(flt)
    return history
def winrateScreen():
    winrate = Screen(name="Winrate")
    winrate.add_widget(Label(text="3"))
    return winrate
def decoderScreen():
    decoder = Screen(name="Decoder")
    decoder.add_widget(Label(text="1"))
    return decoder    
def root():
    flt = FloatLayout()
    top = topWidget()
    
    sm = ScreenManager(size_hint=(1, 0.896),pos_hint={'x':0, 'y':0},transition=FadeTransition())
    tabs = tabsWidget(sm)
    
    history = historyScreen()
    winrate = winrateScreen()
    decoder = decoderScreen()

    
    sm.add_widget(history)
    sm.add_widget(winrate)
    sm.add_widget(decoder)



    flt.add_widget(top)
    flt.add_widget(tabs)
    flt.add_widget(sm)

    return flt


class GUI(App):
    def build(self):
        return root()

GUI().run()  
