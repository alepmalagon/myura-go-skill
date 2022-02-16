from adapt.intent import IntentBuilder
from mycroft import MycroftSkill, intent_handler
from mycroft.util.parse import extract_datetime, extract_number, extract_numbers
import requests
import json
import math

class MyuraGo(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler(IntentBuilder('PositionIntent').require('PositionKeyword'))
    def handle_position_myura(self, message):
        myura_url = self.settings.get('myura_url')

        utterance = message.data.get('utterance')
        position = extract_numbers(utterance)
        if len(position)<2:
            self.speak('I need more numbers')
            return
        elif len(position)<3:
            position.append(6)

        payload = json.dumps({'target':position[:3], 'planner': False})
        self.speak_dialog('GoMyura')
        requests.post(myura_url+'/goto', data = payload)

    @intent_handler(IntentBuilder('MoveIntent').require('MoveKeyword'))
    def handle_move_myura(self, message):
        myura_url = self.settings.get('myura_url')

        utterance = message.data.get('utterance')
        first, *middle, last = utterance.split()
        if last!="start":
            r = requests.get(myura_url+'/landmarks')
            rjson = r.json()
            destination = rjson[last]

            if not destination:
                self.speak_dialog("I don't know that place")
                return

            coords = destination['geometry']['coordinates'][0][0]
            coords.append(10)
        else:
            coords = [0,0,10]
        payload = json.dumps({'target':coords[:3], 'planner': False})
        self.speak_dialog('GoMyura')
        requests.post(myura_url+'/goto', data = payload)

    @intent_handler(IntentBuilder('GoIntent').require('GoKeyword'))
    def handle_go_myura(self, message):
        myura_url = self.settings.get('myura_url')

        utterance = message.data.get('utterance')
        distance = extract_number(utterance)
        if not distance:
            self.speak_dialog("give me numbers!")
            return
        words = utterance.split()
        angle = 0.0
        if 'forward' in words:
            angle = 0.0;
        elif 'backwards' in words:
            angle = 2*math.pi;
        elif 'left' in words:
            angle = 3/2*math.pi;
        elif 'right' in words:
            angle = 1/2*math.pi;
        r = requests.get(myura_url+'/odometry')
        rjson = r.json()
        theta = rjson["theta"] 
        x = rjson["x"] 
        y = rjson["y"] 
        turn = theta - angle
        next_x = x + math.cos(turn)*distance
        next_y = y + math.sin(turn)*distance

        coords = [next_x,next_y,10]
        payload = json.dumps({'target':coords[:3], 'planner': False})
        self.speak_dialog('GoMyura')
        requests.post(myura_url+'/goto', data = payload)

def create_skill():
    return MyuraGo()
