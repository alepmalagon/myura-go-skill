from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
import requests

class MyuraGo(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder('GoIntent').require('GoKeyword'))
    def handle_go_myura(self, message):
        payload = json.dumps({'target':[1,0,6], 'planner': False})
        requests.post('http://10.42.0.146:5000/goto', data = payload)
        self.speak_dialog('go.myura')


def create_skill():
    return MyuraGo()

