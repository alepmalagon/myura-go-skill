from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
import requests
import json

class MyuraGo(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder('GoIntent').require('GoKeyword'))
    def handle_go_myura(self, message):
        #myura_url = self.settings.get('myura_url')
        payload = json.dumps({'target':[1,0,6], 'planner': False})
        self.speak_dialog('go.myura')
        requests.post('http://192.168.10.74:5000/goto', data = payload)


def create_skill():
    return MyuraGo()

