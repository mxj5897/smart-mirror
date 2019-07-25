import datetime
import constants
import kivy
from apiCalls import apiCalls
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.widget import  Widget
from kivy.clock import Clock
from kivy.properties import StringProperty, ObjectProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen

#TODO: Figure out way to scale text with window size
#TODO: Screenmanager for pagination
#TODO: Scheduling of API calls

class mirrorWidget(Widget):
    clock_time_input = StringProperty()
    init_greeting = StringProperty()
    wise_quote = StringProperty()
    screen_manager = ObjectProperty(None)
    screen_page = 0

    def __init__(self, *args, **kwargs):
        super(mirrorWidget, self).__init__(*args, **kwargs)
        init_call = apiCalls()
        self.init_greeting = constants.GREETING
        quote = init_call.quoteAPICall()
        if quote is not None:
            self.wise_quote = quote[0] + "\n -" + quote[1]
        Clock.schedule_interval(self.getTime, 1)

    def on_state(self, instance, value):
        if value == 'home':
            self.screen_manager.current = 'home'

    # handles the logic for switching screens
    def switchScreen(self):
        total_screens = 5
        self.screen_page += 1
        if self.screen_page > total_screens:
            self.screen_page = 0
        pages = {
            0: "home",
            1: "weather",
            2: "task",
            3: "spotify",
            4: "news",
            5: "dict",
            6: "settings"
        }
        self.screen_manager.current = pages.get(self.screen_page, "main")

    # Function which will handle the scheduling of all apps
    def updateEverything(self):
        pass

    # Updates the clock widget with the current date day and time
    def getTime(self, arg):
        current = datetime.datetime.now()
        date = current.strftime("%B %d, %Y")
        day = current.strftime("%A")
        time = current.strftime("%I:%M %p")
        if time[0] == "0":
            time = time[1:]
        self.clock_time_input = time + "\n" + day + "\n" + date

    # Update API calls that are called daily
    # Should includes quote and weather
    def getDailyAPIs(self):
        call = apiCalls()
        quote = call.quoteAPICall()
        if quote is not None:
            print(quote)
            self.wise_quote = quote[0] + "\n -" + quote[1]


class mirrorApp(App):
    def build(self):
        return mirrorWidget()


if __name__ == '__main__':
    mirrorApp().run()
