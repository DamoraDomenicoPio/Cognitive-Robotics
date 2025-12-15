from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

import json

from .NumberPeopleClass import NumberPeopleClass


jsonString = open("log.json", "r").read().replace("\n", "")
personList = json.loads(jsonString)
class ActionNumberPeople(Action):

    def name(self) -> Text:
        return "action_number_people"

    

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:  
        
        person_list = personList["people"].copy()

        number_people = NumberPeopleClass(tracker, person_list)

        number_people.print_entities()
        
        message = number_people.find_people()

        dispatcher.utter_message(text=number_people.get_sentece())

        return [AllSlotsReset()]
