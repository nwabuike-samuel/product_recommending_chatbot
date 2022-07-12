# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset
from xml.dom.xmlbuilder import DocumentLS
from pymongo import MongoClient
from random import randint
import csv, re, dotenv, os
import pymongo
import certifi

dotenv.load_dotenv()
# CONNECTION_STRING = os.environ["CONNECTION_STRING"]
# client = MongoClient(CONNECTION_STRING)
CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.5.0"
client = MongoClient(CONNECTION_STRING)#,  tlsCAFile=certifi.where())
db = client.store
stock = db.stock
association = db.association


class ActionCheckAvailability(Action):
    def name(self) -> Text:
        return "action_check_availability"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: DomainDict) -> List[Dict[Text, Any]]:
        
        requested_product = tracker.get_slot("groceries")
        print(requested_product)
        docs = stock.find({"item":requested_product})
        docs = list(docs)
        print(requested_product)
        # dispatcher.utter_message(text=requested_product)
        # dispatcher.utter_message(text=docs)
        product_available = tracker.get_slot("product_available")

        if len(docs) == 0:
            product_available = False
            #dispatcher.utter_message("no item")
            return [SlotSet("product_available", product_available)]
            #quit()
        for doc in docs:
            if doc["stock"] == 0:
                #current_stock = doc["item"] + " is out of stock"
                product_available = False
                #dispatcher.utter_message("finished")
                return [SlotSet("product_available", product_available)]
            else:
                #current_stock = "We have " + str(doc["stock"]) +" "+ doc["item"] + "s in stock"
                product_available = True
                #dispatcher.utter_message("available")
                print(product_available)
                return [SlotSet("product_available", product_available)]

        #utter_availabile_stock = current_stock
            # print("We have " + str(doc["stock"]) +" "+ doc["item"] + "s in stock")
            
        # dispatcher.utter_message(text=product_available)


class ActionConfirmRequest(Action):
    def name(self) -> Text:
        return "action_confirm_request"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: DomainDict) -> List[Dict[Text, Any]]:
            
            requested_product = tracker.get_slot("groceries")
            stock_amount = tracker.get_slot("stock_amount")# dont forget to name the stock number slot
            docs = stock.find({"item":requested_product})
            docs = list(docs)

            #if availability_check == True: 
            # reduce stock id
            docs = docs[0] 
            try:
                stock.update_one({"item": requested_product}, {"$inc":{"stock":- stock_amount}})
                print("We have " + str(docs["stock"] - stock_amount) +" "+ docs["item"] + "s in stock")
            except Exception as e:
                print(e)

            # display product: options -> buy or add_to_cart

            # need for cart DB?

            #else: unavailable message...already in availability class
            # action_recommend_product

            # Pass docs = stock.find as an argument
            dispatcher.utter_message(text="Do you wish to buy or add to your cart?")

            # dispatcher.utter_button_message("Choose Option", [
            #     {"payload": "/buy", "title": "Buy"},
            #     {"payload": "/add_to_cart", "title": "Add to Cart"}
            # ])

            return []


class ActionRecommendProduct(Action):
    def name(self) -> Text:
        return "action_recommend_product"
    
    def run(self, dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: DomainDict) -> List[Dict[Text, Any]]:
        # if availabiltiy_check == True, 
        # take the grocery slot and find the association with confidence > lorem ipsum
        recommended_product = ""
        requested_product = tracker.get_slot("groceries")
        docs = list(association.find({"antecedents":requested_product, "confidence":{"$gte":0.1}}))
        for doc in docs[:3]:
            try:
                print(doc["consequents"])
            except IndexError:
                break
        # print "Would you consider getting (recommended)"
        try:
            recommendation1 = docs[0]["consequents"]
            #recommended_product = recommendation1
        except IndexError: # No consequent in the rules
            recommended_product = f"What else would you like to get?"
        except UnboundLocalError:
            recommended_product = f"What else would you like to get?"
        recommended_product = (f"Would you consider getting {recommendation1}?")# try item-based collaborative filtering to recommend what customers are currently purchasing
        if len(docs) > 1:
            recommendation2 = docs[1]["consequents"]
            recommended_product += f" or {recommendation2}?"

        dispatcher.utter_message(recommended_product)
        
        return [AllSlotsReset()]

# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []
