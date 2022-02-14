from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler


class MyuraGo(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder('GoIntent').require('GoKeyword'))
    def handle_go_myura(self, message):

        self.speak_dialog('go.myura')


def create_skill():
    return MyuraGo()

