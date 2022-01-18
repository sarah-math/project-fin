# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from dateutil import parser

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

from actions.parsing import (
    parse_duckling_time_as_interval,
    parse_duckling_time,
    get_entity_details,
    parse_duckling_currency,
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
#action_transaction_search

class ActionTransactionSearch(Action):
    """Searches for a transaction"""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_transaction_search"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""
        slots = {
            "AA_CONTINUE_FORM": None,
            "confirmation": None,
            "time": None,
            "time_formatted": None,
            #"start_time": None,
            #"end_time": None,
            # "start_time_formatted": None,
            # "end_time_formatted": None,
            # "grain": None,
            "search_type": None,
            "vendor_name": None,
        }

        if tracker.get_slot("confirmation") == "yes":
            search_type = tracker.get_slot("search_type")
            deposit = search_type == "deposit"
            vendor = tracker.get_slot("vendor_name")
            vendor_name = f" at {vendor.title()}" if vendor else ""
            #start_time = parser.isoparse(tracker.get_slot("start_time"))
            #end_time = parser.isoparse(tracker.get_slot("end_time"))

            numtransacts=5
            total=120
            
            #transactions = profile_db.search_transactions(
            #    tracker.sender_id,
            #     start_time=start_time,
            #     end_time=end_time,
            #     deposit=deposit,
            #     vendor=vendor,
            # )

        #     aliased_transactions = transactions.subquery()
        #     total = profile_db.session.query(
        #         sa.func.sum(aliased_transactions.c.amount)
        #     )[0][0]
        #     if not total:
        #         total = 0
        #     numtransacts = transactions.count()
            slotvars = {
                "total": f"{total:.2f}",
                "numtransacts": numtransacts,
                #"start_time_formatted": tracker.get_slot("start_time_formatted"),
                #"end_time_formatted": tracker.get_slot("end_time_formatted"),
                "vendor_name": vendor_name,
            }
            dispatcher.utter_message(
                    response=f"utter_found_{search_type}_transactions",
                    **slotvars, )

            # dispatcher.utter_message(
            #     response=f"utter_searching_{search_type}_transactions",
            #     **slotvars,
            # )
        #     dispatcher.utter_message(
        #         response=f"utter_found_{search_type}_transactions", **slotvars
        #     )
        # else:
        #     dispatcher.utter_message(response="utter_transaction_search_cancelled")
       
             
        return [SlotSet(slot, value) for slot, value in slots.items()]



class ActionAskTransactionSearchFormConfirm(Action):
    """Asks for the 'zz_confirm_form' slot of 'transaction_search_form'

    A custom action is used instead of an 'utter_ask' response because a different
    question is asked based on 'search_type' and 'vendor_name' slots.
    """

    def name(self) -> Text:
        return "action_ask_transaction_search_form_confirmation"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the custom action"""
        search_type = tracker.get_slot("search_type")
        vendor_name = tracker.get_slot("vendor_name")
        start_time_formatted = tracker.get_slot("start_time_formatted")
        end_time_formatted = tracker.get_slot("end_time_formatted")

        if vendor_name:
            vendor_name = f" with {vendor_name}"
        else:
            vendor_name = ""
        if search_type == "spend":
            text = (
                f"Do you want to search for transactions{vendor_name} between "
                f"{start_time_formatted} and {end_time_formatted}?"
            )
        elif search_type == "deposit":
            text = (
                f"Do you want to search deposits made to your account between "
                f"{start_time_formatted} and {end_time_formatted}?"
            )
        buttons = [
            {"payload": "/affirm", "title": "Yes"},
            {"payload": "/deny", "title": "No"},
        ]

        dispatcher.utter_message(text=text, buttons=buttons)

        return []




class ActionPayCC(Action):
    """Pay credit card."""

    def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_pay_cc"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict]:
        """Executes the action"""

        slots = {
            "AA_CONTINUE_FORM": None,
            "confirmation": None,
            "credit_card": None,
            "account_type": None,
            "amount-of-money": None,
            "time": None,
            #"time_formatted": None,
            # "start_time": None,
            # "end_time": None,
            # "start_time_formatted": None,
            # "end_time_formatted": None,
            # "grain": None,
            #"number": None,
        }

        if tracker.get_slot("confirmation") == "yes":
            credit_card = tracker.get_slot("credit_card")
            amount_of_money = float(tracker.get_slot("amount-of-money"))
            #amount_transferred = float(tracker.get_slot("amount_transferred"))
            """profile_db.pay_off_credit_card(
                tracker.sender_id, credit_card, amount_of_money
            )"""

            dispatcher.utter_message(response="utter_cc_pay_scheduled")

            #slots["amount_transferred"] = amount_transferred + amount_of_money
        else:
            dispatcher.utter_message(response="utter_cc_pay_cancelled")

        return [SlotSet(slot, value) for slot, value in slots.items()]

class ActionAddRecipient(Action):
     
     def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_add_person_to_recipients"

     async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the action"""
        slots = {
          
           "confirmation": None,
           "PERSON_Recipient": None,
           "RIB": None,
           "number": None,
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

            dispatcher.utter_message(response="utter_recipients_complete")

#            amount_transferred = float(tracker.get_slot("amount_transferred"))
           
#            slots["amount_transferred"] = amount_transferred + amount_of_money
            #slots["amount_transferred"] = 150
        else:
            dispatcher.utter_message(response="utter_recipients_cancelled")
                                               
        
        #return []
        return [SlotSet(slot, value) for slot, value in slots.items()]

class ActionTransferMoney(Action):
     
     def name(self) -> Text:
        """Unique identifier of the action"""
        return "action_transfer_money"

     async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """Executes the action"""
        slots = {
          # "AA_CONTINUE_FORM": None,
           "confirmation": None,
           "PERSON_transfer": None,
           "amount-of-money": None,
            "number": None,
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
            #slots["amount_transferred"] = 150
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
            
            #SlotSet("account_type", value=None)

                
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