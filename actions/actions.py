# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Action
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
    UserUtteranceReverted,
)


#
#class ActionHelloWorld(Action):
#
#    def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionTransferMoney(Action):
     
     def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_transfer_money"

     async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the action"""
    #    slots = {
           # "AA_CONTINUE_FORM": None,
    #       "confirmation": None,
    #       "PERSON_transfer": None,
    #       "amount-of-money": None,
           # "number": None,
#   }

        if tracker.get_slot("confirmation") == "yes":
#            amount_of_money = float(tracker.get_slot("amount-of-money"))
#            from_account_number = profile_db.get_account_number(
#                profile_db.get_account_from_session_id(tracker.sender_id)
#            )
#            to_account_number = profile_db.get_account_number(
#                profile_db.get_recipient_from_name(
#                    tracker.sender_id, tracker.get_slot("PERSON")
#                )
#            )
#            profile_db.transact(
#                from_account_number,
#                to_account_number,
#                amount_of_money,
#            )

            dispatcher.utter_message(response="utter_transfer_complete")

#            amount_transferred = float(tracker.get_slot("amount_transferred"))
#            slots["amount_transferred"] = amount_transferred + amount_of_money
        else:
            dispatcher.utter_message(response="utter_transfer_cancelled")
        
        return []
#        return [SlotSet(slot, value) for slot, value in slots.items()]
