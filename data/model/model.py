from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')

data = {}

def createDataBase(data):
    db = client.mars
    db.insights.drop()
    db.insights.insert(data)


def getStoredData():
    db = client.mars
    values = [element for element in db.insights.find({}, {'_id': 0})]
    data = values[0]
    return values
