from mycroft import MycroftSkill, intent_file_handler


class MyuraGo(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('go.myura.intent')
    def handle_go_myura(self, message):
        self.speak_dialog('go.myura')


def create_skill():
    return MyuraGo()

