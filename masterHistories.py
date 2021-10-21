from dataModels import *
from bson.json_util import dumps, loads
import json, pymongo

import logging 
logging.basicConfig(format='%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',level=logging.INFO,filename='trendTracker.log')
logger = logging.getLogger('trendTracker')

###################
def configIndex():
    try:        
        result = dbHistory.create_index([("id", pymongo.DESCENDING),("symbol", pymongo.DESCENDING)],unique=True)
        return True
    except Exception as e:
        logger.error(f"An Error occured :: {e}")
        return False

def updateHistory(coin):
    try:
        id = coin["id"]    
        query = {"id": id}        
        set = {"$set": coin}
        result = dbHistory.update_many(query,set,upsert=True)
        return result
    except Exception as e:
        logger.error(f"An Error occured :: {e}")
        return False

def insertHistory(coin):
    try:
        id = coin["id"]    
        updateTime = coin["updateTime"]    
        query = {"id": id, "updateTime": updateTime}        
        set = {"$set": coin}
        result = dbHistory.update_many(query,set,upsert=True)
        return result
    except Exception as e:
        logger.error(f"An Error occured :: {e}")
        return False

def searchHistory(symbol=None):
    try:        
        if symbol is None :
            result = dbHistory.find()
        if symbol is not None :
            symbol = symbol.lower()            
            query = {"$or":[{"id": symbol},{"name": symbol},{"symbol":symbol}]}
            result = dbHistory.find(query)        
        # listTrend = []
        # for item in result:
        #     listTrend.append(item)    
        # return listTrend        
        return result
    except Exception as e:
        logger.error(f"An Error occured :: {e}")
        return False

def deleteHistory(symbol=None):
    try:
        if symbol is None:
            dbHistory.delete_many({})
        elif symbol is not None:
            query = {"id": symbol}
            dbHistory.delete_many(query)
        return True
    except:
        return False

def updateHistorySupportResistance(coin):
    try:
        id = coin["id"]
        updateTime = coin["updateTime"]
        supports = coin["supports"]
        support = coin["support"]
        resistance = coin["resistance"]
        percent_2_resistance = coin["percent_2_resistance"]

        query = {"id": id}        
        set = {"$set": {"supports": supports,
                        "support": support,
                        "resistance": resistance,
                        "updateTime": updateTime,
                        "percent_2_resistance": percent_2_resistance}}
                        
        result = dbHistory.update_many(query,set,upsert=True)
        return result
    except Exception as e:
        logger.error(f"An Error occured :: {e}")
        return False

def searchTopCap():
    try:
        query = {"market_cap_rank":{"$lte": 10}}
        result = dbHistory.find(query).sort("market_cap_rank")
        return result

    except Exception as e:
        logger.error("An Error occured on searchTopCap :: ", e)
        return False

def searchBest():
    try:        
        querySort = "price_change_percentage_1h"
        result = dbHistory.find().sort(querySort,-1).limit(10)
        return result

    except Exception as e:
        print("An Error occured :: ", e)
        return False

def searchWorst():
    try:        
        querySort = "price_change_percentage_1h"
        result = dbHistory.find().sort(querySort).limit(10)
        return result

    except Exception as e:
        print("An Error occured :: ", e)
        return False

def searchSuggest():
    try:                
        query = {"$or":[{"percent_2_resistance":{"$lte": 5,"$gte": -5}},{"percent_2_resistance":{"$lte": 105,"$gte": 95}}]}
        result = dbHistory.find(query).sort("percent_2_resistance")
        return result

    except Exception as e:
        print("An Error occured :: ", e)
        return False


def main():
    print("masterHistory")
    # searchBest()
    # deleteTrend()
    # configIndex()      
    # deleteHistory()  
    print(searchWorst())
    

if __name__ == "__main__":
    main()
