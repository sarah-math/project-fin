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
        slots = {
           "AA_CONTINUE_FORM": None,
           "confirmation": None,
           "PERSON_transfer": None,
           "amount-of-money": None,
           # "number": None,
   }

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
            slots["amount_transferred"] = 150
        else:
            dispatcher.utter_message(response="utter_transfer_cancelled")
        
        #return []
        return [SlotSet(slot, value) for slot, value in slots.items()]



class ActionShowTransferCharge(Action):
    """Lists the transfer charges"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_show_transfer_charge"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the custom action"""
        dispatcher.utter_message(response="utter_transfer_charge")

        events = []
        active_form_name = tracker.active_form.get("name")
        if active_form_name:
            # keep the tracker clean for the predictions with form switch stories
            events.append(UserUtteranceReverted())
            # trigger utter_ask_{form}_AA_CONTINUE_FORM, by making it the requested_slot
            events.append(SlotSet("AA_CONTINUE_FORM", None))
            # # avoid that bot goes in listen mode after UserUtteranceReverted
            events.append(FollowupAction(active_form_name))

        return events

class ActionShowRecipients(Action):
    

    def name(self) -> Text:
       
        return "action_show_recipients"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the custom action"""
        dispatcher.utter_message(response="utter_recipients")

        events = []
        active_form_name = tracker.active_form.get("name")
        if active_form_name:
            # keep the tracker clean for the predictions with form switch stories
            events.append(UserUtteranceReverted())
            # trigger utter_ask_{form}_AA_CONTINUE_FORM, by making it the requested_slot
            events.append(SlotSet("AA_CONTINUE_FORM", None))
            # # avoid that bot goes in listen mode after UserUtteranceReverted
            events.append(FollowupAction(active_form_name))

        return events


class ActionShowBalance(Action):
    """Shows the balance of bank or credit card accounts"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_show_balance"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the custom action"""
        account_type = tracker.get_slot("account_type")

        if account_type == "credit":
            # show credit card balance
            credit_card = tracker.get_slot("credit_card")
            #available_cards = profile_db.list_credit_cards(tracker.sender_id)

            """if credit_card and credit_card.lower() in available_cards:
                current_balance = profile_db.get_credit_card_balance(
                    tracker.sender_id, credit_card
                )"""
            current_balance= 2000
            dispatcher.utter_message(
                response="utter_credit_card_balance",
                **{
                    "credit_card": credit_card.title(),
                    "credit_card_balance": f"{current_balance:.2f}",
                }, )
            events = []
         #   events.append(SlotSet("account_type", value=None))

                
            """else:
                for credit_card in profile_db.list_credit_cards(tracker.sender_id):
                    current_balance = profile_db.get_credit_card_balance(
                        tracker.sender_id, credit_card
                    )
                    dispatcher.utter_message(
                        response="utter_credit_card_balance",
                        **{
                            "credit_card": credit_card.title(),
                            "credit_card_balance": f"{current_balance:.2f}",
                        },
                    )"""
        else:
            # show bank account balance
            """account_balance = profile_db.get_account_balance(tracker.sender_id)
            amount = tracker.get_slot("amount_transferred")
            if amount:
                amount = float(tracker.get_slot("amount_transferred"))
                init_account_balance = account_balance + amount
                dispatcher.utter_message(
                    response="utter_changed_account_balance",
                    init_account_balance=f"{init_account_balance:.2f}",
                    account_balance=f"{account_balance:.2f}",
                )
            else:
                dispatcher.utter_message(
                    response="utter_account_balance",
                    init_account_balance=f"{account_balance:.2f}",
                )"""
            account_balance= 5000
            dispatcher.utter_message(
                    response="utter_account_balance",
                    init_account_balance=f"{account_balance:.2f}",
                )

        events = []
        active_form_name = tracker.active_form.get("name")
        if active_form_name:
            # keep the tracker clean for the predictions with form switch stories
            events.append(UserUtteranceReverted())
            # trigger utter_ask_{form}_AA_CONTINUE_FORM, by making it the requested_slot
            events.append(SlotSet("AA_CONTINUE_FORM", None))
            # avoid that bot goes in listen mode after UserUtteranceReverted
            events.append(FollowupAction(active_form_name))

        return events