import datetime as dt 
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset

import json 

class ActionFindPerson(Action):


    def name(self) -> Text:
        return "action_find_person"
    
    def get_response(self, roi1_time, roi2_time, default_location, roi1, roi2):
        position = ''
        # position = '(id '+str(id)+')'
        if roi1_time > 0: 
            position += 'who was in '+roi1+' for '+str(roi1_time)+' minutes'
        if roi1_time>0 and roi2_time>0:
            position +=' and '
        if roi2_time>0: 
            position += 'who was in '+roi2+' for '+str(roi2_time)+ ' minutes'
        if roi1_time==0 and roi2_time==0:
            position = 'who was in '+default_location

        position = position+'...'
        return position

    def dict_compare(self, chat, log, id): 
        res = True
        log['bag'] = str(log['bag']).lower()
        log['hat'] = str(log['hat']).lower()
        if chat['gender']!='unknown' and chat['gender']!=log['gender']:
            res = False
        if chat['upper_color']!='unknown' and chat['upper_color']!=log['upper_color']:
            res = False
        if chat['lower_color']!='unknown' and chat['lower_color']!=log['lower_color']:
            res = False 
        if chat['bag_presence']!='unknown' and chat['bag_presence']!=log['bag']:
            res = False
        if chat['hat_presence']!='unknown' and chat['hat_presence']!=log['hat']:
            res = False

        if res == True:
            print('\n ---- ID = '+str(id)+'\nchat:')
            print(str(chat))
            print('\nlog: ')
            print(str(log))
        return res


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:



        # Lettura degli slot 
        g = tracker.get_slot("gender")
        if g == 'False': 
            gender = 'female'
        else: 
            gender = 'male'
        print("gender: " + str(gender))
        upper_color = tracker.get_slot("upper_color")
        print("upper_color: " + str(upper_color))
        upper_cloth = tracker.get_slot("upper_cloth")
        print("upper_cloth: " + str(upper_cloth))
        lower_color = tracker.get_slot("lower_color")
        print("lower_color: " + str(lower_color))
        lower_cloth = tracker.get_slot("lower_cloth")
        print("lower_cloth: " + str(lower_cloth))
        hat_presence = tracker.get_slot("hat_presence")
        print("hat_presence: " + str(hat_presence))
        bag_presence = tracker.get_slot("bag_presence")
        print("bag_presence: " + str(bag_presence))

        # letturs del file
        FILE_NAME = 'log.json'
        roi1 = 'bar'
        roi2 = 'unisa store'
        default_location = 'mall'

        with open(FILE_NAME, 'r') as file:
            list = json.load(file)

        positions = {}
        message = ''
        for person in list['people']:
            # print(str(type(person['bag']))+str(person['bag']))

            chat = {}
            chat['gender'] = gender
            chat['upper_color'] = upper_color
            chat['lower_color'] = lower_color
            chat['bag_presence'] = bag_presence
            chat['hat_presence'] = hat_presence
            id = person['id']
            if self.dict_compare(chat, person, id) == True:
                # scrittura della risposta 
                print('SCRIVO UNA RISPOSTA  '+str(id))
                roi1_time = person['roi1_persistence_time']
                roi2_time = person['roi2_persistence_time']
                positions[id] = self.get_response(roi1_time, roi2_time, default_location, roi1, roi2)
                
        # print(str(positions))
        if len(positions) > 0: 
                message = 'Yes, I saw someone like you described '
                i = 0
                for position in positions:
                    if i > 0: 
                        message += ' I also found someone matching you description '
                    message += positions[position]
                    i = i+1
                # print('id = '+str(id)+' ')
        else: 
            message = 'I\'m sorry, I couldn\'t find anyone matching you description'
      

        dispatcher.utter_message(text=message)

        return [AllSlotsReset()]
