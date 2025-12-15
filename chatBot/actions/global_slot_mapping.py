from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, Action
from rasa_sdk.events import EventType
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

class GlobalSlotMapping(Action):


    def name(self) -> Text:
        return "global_slot_mapping"


    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        new_slot_values: Dict[Text, Any] = dict()

        entities = tracker.latest_message['entities']


        for i in range(len(entities)):
            entity = entities[i]['entity']
            value = entities[i]['value']   
            # clothes colors
            if i < len(entities)-1: 
                nextEntity = entities[i+1]['entity']
                if entity == 'color':
                    if nextEntity == 'upper_cloth':
                        new_slot_values['upper_color'] = value
                    elif nextEntity == 'lower_cloth':
                        new_slot_values['lower_color'] = value
                    if entity == 'hat_presence' or entity=='hat_presence':
                        new_slot_values[entity] = value
            
            # look for negation
            if i > 0:
                prevEntity = entities[i-1]['entity']
                if entity == 'hat_presence' or entity == 'bag_presence': 
                    if prevEntity == 'negation':
                        new_slot_values[entity] = 'false'
                    else: 
                        new_slot_values[entity] = 'true'
                elif entity == 'color' and prevEntity == 'negation' and i<len(entities)-1: 
                    if nextEntity == 'upper_cloth':
                        new_slot_values['upper_color'] = 'not_'+value
                    elif nextEntity == 'lower_cloth': 
                        new_slot_values['lower_color'] = 'not_'+value
            



        print('Global slot mapping: '+str(new_slot_values))
        return [
            SlotSet(name, value)
            for name, value in new_slot_values.items()
        ]