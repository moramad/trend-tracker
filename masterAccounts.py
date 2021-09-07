from dataModels import *
from bson.json_util import dumps, loads
import json, pymongo

def configIndex():
    try:        
        result = dbAccount.create_index([("username", pymongo.DESCENDING), ("email", pymongo.ASCENDING)],unique=True)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def registerAccounts(account):    
    try:          
        result = dbAccount.insert_one(account)
        return True
    except pymongo.errors.DuplicateKeyError:
        return False
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def unregisterAccounts(query=None):    
    try:           
        if query is None :
            result = dbAccount.delete_many({})
        if query is not None :
            result = dbAccount.delete_many(query)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

    # bentuk resultnya macem apa, misal status success.
    return result

def enableAccounts(query=None):
    set = {
        "$set": {
            "active" : True
        }
    }    

    try:        
        if query is None :
            result = dbAccount.update_many({}, set)
        if query is not None :
            result = dbAccount.update_many(query, set)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def disableAccounts(query=None):
    set = {
        "$set": {
            "active" : False
        }
    }    

    try:        
        if query is None :
            result = dbAccount.update_many({}, set)
        if query is not None :
            result = dbAccount.update_many(query, set)
        return True
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def searchAccounts(query=None):
    try:        
        if query is None :
            result = dbAccount.find()
        if query is not None :
            result = dbAccount.find(query)
        list_result = list(result)
        json_data = dumps(list_result)
        return json_data
    except Exception as e:
        print("An Error occured :: ", e)
        return False

def main():    
    # configIndex()
    # unregisterAccounts()
    account = Accounts("mochamad","rama","mochamad@ramadhan.com","pass1234","admin",True)
    print(registerAccounts(account))
    
    # print("masterAccounts")

if __name__ == "__main__":
    main()