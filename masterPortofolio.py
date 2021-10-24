from dataModels import *
from datetime import datetime
from bson.json_util import dumps, loads
import json, pymongo

import logging 
logging.basicConfig(format='%(asctime)s %(levelname)-4s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',level=logging.INFO,filename='trendTracker.log')
logger = logging.getLogger('trendTracker')

###################
# FORMAT STRUCTURE JSON MasterPortofolio

# id = "btc"
# mockup = {}
# mockup.update({"id": id.lower()})
# mockup.update({"avgPrice": 1000})
# mockup.update({"totalCoin": 1})

# transID = 1
# transaction = {}
# transaction.update({"transID": transID})
# transaction.update({"transDate": datetime.today()})
# transaction.update({"numberCoin": 1})
# transaction.update({"avgPrice": 1000})
# transaction.update({"transType": "buy"})

###################
def configIndex():
    try:        
        result = dbPortofolio.create_index([("id", pymongo.DESCENDING),("symbol", pymongo.DESCENDING)],unique=True)
        return True
    except Exception as e:
        logger.error(f"An Error occured in configIndex :: {e}")
        return False

def updatePortofolio(coin):
    try:
        id = coin["id"]    
        query = {"id": id}        
        set = {"$set": coin}
        result = dbPortofolio.update_many(query,set,upsert=True)
        return result
    except Exception as e:
        print(f"An Error occured in updatePortofolio :: {e}")
        logger.error(f"An Error occured in updatePortofolio :: {e}")
        return False    

def updateTransaction(coin,trans):
    try:        
        id = coin["id"]
        transID = trans["transID"]
        query = {"id": id, "trans.transID": transID}
        set = {"$set": coin,
                "$push": {
                "trans": {
                    "$each": [trans],
                    "$sort": { "transID": 1 },
                }
            }
        }
        result = dbPortofolio.update_many(query,set,upsert=True)
        return result
    except Exception as e:
        logger.error(f"An Error occured in updateTransaction :: {e}")
        print(f"An Error occured in updateTransaction :: {e}")
        return False

def searchTransaction():
    try:
        query = {"id": id}
        result = dbPortofolio.find(query)
        for item in result:            
            print(item)
        return result

    except Exception as e:
        print("An Error occured on searchTransaction :: ", e)
        logger.error("An Error occured on searchTransaction :: ", e)
        return False    

if __name__ == "__main__":
    print("OK")
    # print(updatePortofolio(mockup))
    # print(updateTransaction(mockup,transaction))
    # searchTransaction()