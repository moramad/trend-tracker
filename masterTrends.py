from dataModels import *
from bson.json_util import dumps, loads
import json, pymongo

###################
def configIndex():
    try:        
        result = dbTrend.create_index([("id", pymongo.DESCENDING),("symbol", pymongo.DESCENDING)],unique=True)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def updateTrend(coin):
    try:
        id = coin["id"]    
        query = {"id": id}        
        set = {"$set": coin}
        result = dbTrend.update_many(query,set,upsert=True)
        return result
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def updateHistory(coin):
    try:
        id = coin["id"]    
        updateTime = coin["updateTime"]    
        query = {"id": id, "updateTime": updateTime}        
        set = {"$set": coin}
        result = dbHistory.update_many(query,set,upsert=True)
        return result
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def updateTrendSupports(coin):
    try:
        id = coin["id"]
        updateTime = coin["updateTime"]
        supports = coin["supports"]

        query = {"id": id}        
        set = {"$set": {"supports": supports,
                        "updateTime": updateTime}}
                        
        result = dbTrend.update_many(query,set,upsert=True)
        return result
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def updateParsialTrend(coin):
    try:
        id = coin["id"]        
        query = {"id": id}        
        set = {"$set": {"asset_platform_id": "test"}}
        result = dbTrend.update_many(query,set,upsert=True)
        return result
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def searchTrend(symbol=None):
    try:        
        if symbol is None :
            result = dbTrend.find()
        if symbol is not None :
            query = {"id": symbol}
            result = dbTrend.find(query)        
        # listTrend = []
        # for item in result:
        #     listTrend.append(item)    
        # return listTrend        
        return result
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def searchHistory(symbol=None):
    try:        
        if symbol is None :
            result = dbHistory.find()
        if symbol is not None :
            query = {"id": symbol}
            result = dbHistory.find(query)        
        # listTrend = []
        # for item in result:
        #     listTrend.append(item)    
        # return listTrend        
        return result
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def deleteTrend(symbol=None):
    try:
        if symbol is None:
            dbTrend.delete_many({})
        elif symbol is not None:
            query = {"id": symbol}
            dbTrend.delete_many(query)
        return True
    except:
        return False

def main():
    print("MasterCoins")
    # deleteTrend()
    # configIndex()    
    # print(searchTrend())
    

if __name__ == "__main__":
    main()