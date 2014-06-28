from pymongo import *


client = MongoClient('localhost', 27017)
db = client['organizer']
