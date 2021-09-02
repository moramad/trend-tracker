from dataModels import *
from bson.json_util import dumps, loads
import json, pymongo

###################
def configIndex():
    try:
        collection = dbSymbol
        result = collection.create_index([("symbolID", pymongo.DESCENDING), ("tickerID", pymongo.ASCENDING)],unique=True)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def registerSymbols(symbol):    
    try:
        collection = dbSymbol    
        result = collection.insert_one(symbol)
        return True
    except pymongo.errors.DuplicateKeyError:
        # symbolID = symbol["symbolID"]
        # print (f"key {symbolID} is duplicate!")
        return False
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def searchSymbols(query=None):
    try:
        collection = dbSymbol
        if query is None :
            result = collection.find()
        if query is not None :
            result = collection.find(query)
        list_result = list(result)
        json_data = dumps(list_result)
        return json_data
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def getListSymbols():
    try:
        collection = dbSymbol
        result = collection.find({}, {'tickerID': 1, '_id': 0})
        list_result = list(result)
        json_data = dumps(list_result)
        return json_data
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def unregisterSymbols(query=None):    
    try:
        collection = dbSymbol    
        if query is None :
            result = collection.delete_many({})
        if query is not None :
            result = collection.delete_many(query)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

    # bentuk resultnya macem apa, misal status success.
    return result

def enableSymbols(query=None):
    set = {
        "$set": {
            "allowUpdate" : True
        }
    }    

    try:
        collection = dbSymbol
        if query is None :
            result = collection.update_many({}, set)
        if query is not None :
            result = collection.update_many(query, set)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def disableSymbols(query=None):
    set = {
        "$set": {
            "allowUpdate" : False
        }
    }    

    try:
        collection = dbSymbol
        if query is None :
            result = collection.update_many({}, set)
        if query is not None :
            result = collection.update_many(query, set)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False


def main():
    # asii = Symbols("ASII","stock",False,"ASII.JK")        
    # print(registerSymbols(asii))
    # print(asii["symbolID"])
    # print(searchSymbols({'symbolID':'ASII'}))
    # print(getListSymbols())
    # unregisterSymbols({'symbolID':'ASII'})
    # unregisterSymbols()
    # configIndex()
    # enableSymbols()
    
    # emittenJSON = json.dumps(emitten)
    # print(emittenJSON)
    # emittenJSONData = json.loads(emittenJSON)
    # print(emittenJSONData['symbolID'])

    with open("coins.idx") as indexCoin:
        for line in indexCoin:
            id = line.strip()
            try:
                print(f"insert data : {id}")
                coin = Symbols(id,"crypto",True,id)
                registerSymbols(coin)
            except:
                print("Error!")

if __name__ == "__main__":
    main()