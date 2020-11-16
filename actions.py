# https://rasa.com/docs/rasa/core/actions/#custom-actions/

from datetime import datetime
from datetime import timedelta
from typing import Any, Text, Dict, List, Text, Union, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.forms import FormAction

import json

from gdrive_service import GDriveService

import logging

logger = logging.getLogger(__name__)

# mbledh informacion mbi studentin dhe llojin e kerkeses 

class ActionKerkeseDokumenti(FormAction):

    def name(self) -> Text:
        return "form_kerkese"

    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return [  
            "emri",
            "mbiemri",
            "dega",
            "vitiStudimit"
        ]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return{
            "emri":[self.from_text()],
            "mbiemri":[self.from_text()],
            "dega": [self.from_text()],
            "vitiStudimit":[self.from_text()]
        }
   
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        emri= tracker.get_slot("emri")
        mbiemri=tracker.get_slot("mbiemri")
        dega= tracker.get_slot("dega")
        vitiStudimit=tracker.get_slot("vitiStudimit")
        dokument=tracker.get_slot("dokument")
        
        dispatcher.utter_message(text="Të dhënat që ju dhatë janë:\nEmri:{}\nMbiemri:{}\nKursi Studimit:{}\nViti i Studimit:{}\n A janë të dhënat e sakta?".format(emri,mbiemri,dega,vitiStudimit))

        dataT=datetime.now()+ timedelta(14)
        dataP=dataT.strftime("%d/%m/%Y")

        return [SlotSet("data", dataP)]
# updaton ne google sheets

class ActionRuajTeDhena(Action):

    def name(self) -> Text:
        return "action_ruajTeDhenat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        import datetime

        emri= tracker.get_slot("emri")
        mbiemri=tracker.get_slot("mbiemri")
        dega= tracker.get_slot("dega")
        vitiStudimit=tracker.get_slot("vitiStudimit")
        dokument=tracker.get_slot("dokument")

        data=datetime.datetime.now().strftime("%d/%m/%Y")
        teDhenat=[emri,mbiemri,dega,vitiStudimit,dokument,data]
        try:
            
            gdrive = GDriveService()
            gdrive.store_data(teDhenat)

            dispatcher.utter_message(template="utter_dataDokumentit")

            return []

        except Exception as e:

            logger.error(
                "Failed to write data to gdocs. Error: {}" "".format(e.message),
                exc_info=True,
            )
            dispatcher.utter_message(template="utter_kerkesauRefuzua")
            return []

# shkruan nje google sheets feedback-un nga studentet mbi asistentin    
        
class ActionFeedback(FormAction):

    def name(self) -> Text:
        return "form_feedback"

    @staticmethod
    def required_slots(tracker)-> List[Text]:
        return ["feedback"]
    
    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return{
            "feedback":[self.from_text()]
        }
   
    def submit(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        feedback= tracker.get_slot("feedback")
        dataK=datetime.now().strftime("%d/%m/%Y")
        komente=[feedback,dataK]
        try:

            gdrive = GDriveService()
            gdrive.store_comments(komente)

            dispatcher.utter_message(template="utter_mirupafshim")

            return []
        except Exception as e:

            logger.error(
                "Failed to write data to gdocs. Error: {}" "".format(e.message),
                exc_info=True,
            )

            dispatcher.utter_message(template="utter_kerkesauRefuzua")
            return []

# shikon se per cfare informacioni pyet studenti dhe kthen pergjigje ne baze te pyetjes 

class ActionChitchat(Action):

    def name(self) -> Text:
        return "action_chitchat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        chitchat=['shërbimet','orari','bursa','dokumentaElektronike','kohëzgjatjaDokumentit','rregjistrimMaster']

        intent = tracker.latest_message['intent'].get('name')

        if intent in chitchat:
            dispatcher.utter_message(template="utter_"+intent)

        return []        

class ActionMbrojtjaGjuhes(Action):

    def name(self) -> Text:
        return "action_mbrojtaGjuhesHuaj"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        gjuha=tracker.get_slot("gjuhaHuaj")

        with open('gjuhetHuaja.json', 'r') as f:
            gjuhet = json.load(f)

        if gjuha!=None:
            gjuha=gjuha.lower()[:-2]
            tekst="Provimet dhe nivelet përkatëse janë:\n"
            for gjuha in gjuhet[gjuha]:
                for provim in gjuha:
                    tekst+="\n"+provim
                    for niveli in gjuha[provim]:
                        tekst=tekst+"\nNiveli "+niveli

        else:
            tekst="Gjuhët e lejuara janë:"
            for gjuha in gjuhet:
                tekst+="\n"+gjuha
                
        dispatcher.utter_message(text=tekst)
        return []        

# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

