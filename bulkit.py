from urllib import response
import requests
import json
import re
# import pycouchdb
from pymongo import MongoClient
import pymongo

connection_string = "mongodb+srv://bulkuser:happy-go-lucky@mtg.uoerg.mongodb.net/MTG?retryWrites=true&w=majority"
api_url = "https://api.scryfall.com/bulk-data/default_cards"

downUrl = requests.get(api_url)
r = downUrl.json()

downLink = r["download_uri"]

print('Downloading file ....')

d = requests.get(downLink)

fileName = downLink.split('/')[-1]
with open(fileName,'wb') as output_file:
    output_file.write(d.content)
print('Download Completed!!!')

cardsList = []
print('Starting to load JSON ...')
i = 0
# server = pycouchdb.Server("http://admin:password@localhost:5984/")
client = MongoClient(connection_string)
# db = server.database("masterdb")
mydb = client["MTG-Master"]
mycol = mydb["cardMaster"]

mycol.drop()

mycol = mydb["cardMaster"]

with open(fileName) as f:
    for jsonObj in f:
        str_obj = str(jsonObj)
        if i == 0:
            i = i + 1
        else:
            rmJson = re.sub(',$', '' , str_obj)
            # print(rmJson)
            try:
                i = i + 1
                print('prosessing line: ', i)
                changed = re.sub('"id"', '"_id"', rmJson)
                # print(changed)
                cardDict = json.loads(changed)
                cardsList.append(cardDict)
                try:
                    # doc = db.save(cardDict)
                    x = mycol.insert_one(cardDict)
                except:
                    print("Unable to add this to the database")
            except:
                print('there was a error with one of the cards, if this is at the end this doesnt matter')