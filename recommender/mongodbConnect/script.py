from pkgutil import get_data
from xml.dom.xmlbuilder import DocumentLS
from pymongo import MongoClient
from random import randint
import csv, re, dotenv, os

dotenv.load_dotenv()


import pymongo
import certifi
#import dns

# Replace the uri string with your MongoDB deployment's connection string.
conn_str = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.5.0"
client = MongoClient(conn_str)#,  tlsCAFile=certifi.where())#, serverSelectionTimeoutMS=5000)

# try:
#     #print(client.server_info())
#     print(client.database_names())
# except Exception as e:
#     # print("Unable to connect to the server.")
#     print(e)

# CONNECTION_STRING = os.environ["CONNECTION_STRING"]
# client = MongoClient(CONNECTION_STRING)
db = client.store
stock = db.stock
association = db.association

#create stock database
with open('recommender\\mongodbConnect\\stock.txt') as file:
    for line in file:
        rng = randint(0, 10)
        stock.insert_one({"item":line.strip(), "stock":rng})


pattern = re.compile(r"frozenset\(\{'(.+)'\}\)")

# store association rules in database
with open('recommender\\mongodbConnect\\rules.csv') as csvFile:
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        data = {}
        data['antecedents'] = re.match(r"frozenset\(\{'(.+)'\}\)", row['antecedents']).group(1)
        data['consequents'] = re.match(r"frozenset\(\{'(.+)'\}\)", row['consequents']).group(1)
        data['support'] = float(row['support'])
        data['confidence'] = float(row['confidence'])
        data['lift'] = float(row['lift'])
        try:
            association.insert_one(data)
        except:
            print(data)

# user_input = input("Enter the name of the item: ")
# amount = int(input(f"How many {user_input} would you like to buy?: "))
# docs = stock.find({"item": user_input})
# docs = list(docs)

# for doc in docs:
#     print("We have " + str(doc["stock"]) +" "+ doc["item"] + "s in stock")
#     print(doc)

# if len(docs) == 0:
#     available = False
#     print(available)
#     print("Item does not exist")
#     #quit()
# for doc in docs:
#     if doc["stock"] == 0:
#         available = False
#         print(available)
#         print(doc["item"] + " is out of stock")
#         quit()
#     else:
#         available = True
#         print(available)
#         print("We have " + str(doc["stock"]) +" "+ doc["item"] + "s in stock")

####reduce stock number
# After confirmed order
# docs = docs[0] 
# try:
#     stock.update_one({"item": user_input}, {"$inc":{"stock":- amount}})
#     print("We have " + str(docs["stock"] - amount) +" "+ docs["item"] + "s in stock")
# except Exception as e:
#     print(e)

# recommend product
# for all association of request
# get confidence > 0.02
# print consequent...recommend

# user_input = "yogurt"

# docs = list(association.find({"antecedents":user_input, "confidence":{"$gte":0.2}}))
# for doc in docs[:4]:
#     try:
#         print(doc["consequents"])
#     except IndexError:
#         break

# recommendation1 = docs[0]["consequents"]
# recommended_product = f"Would you consider getting {recommendation1}"
# if len(docs) > 1:
#     recommendation2 = docs[1]["consequents"]
#     recommended_product += f" or {recommendation2} ?"
# print(recommended_product)