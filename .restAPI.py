from fastapi import FastAPI, status
from bson.json_util import dumps, loads
from typing import Optional
from dataModels import *

app = FastAPI()

@app.get('/symbols', tags=["symbol"])
async def search_symbols(symbolID: Optional[str] = None):
    symbols = []    
    if symbolID:
        query = {'symbolID': symbolID}  
        result = dbSymbol.find(query)
    else:
        result = dbSymbol.find()
    
    for symbol in result:        
        symbols.append(Symbol(**symbol))      
    return {'symbols': symbols}

@app.get('/listSymbols', tags=["symbol"])
async def list_symbols(symbolID: Optional[str] = None):    
    if symbolID:        
        result = dbSymbol.find({'symbolID': symbolID}, {'tickerID': 1, '_id': 0})
        print(result)
        return {'symbols': result[0]}
    else:
        result = dbSymbol.find({}, {'tickerID': 1, '_id': 0})
        symbols = []    
        for symbol in result:         
            symbols.append(symbol)      
        return {'symbols': symbols}    

@app.post('/registerSymbols', tags=["symbol"])
async def register_symbol(symbol: Symbol):
    if hasattr(symbol, 'id'):
        delattr(symbol, 'id')        
    ret = dbSymbol.insert_one(symbol.dict(by_alias=True))
    symbol.id = ret.inserted_id
    return {'symbol': symbol}

@app.post('/enableSymbols', tags=["symbol"])
async def enable_symbol(symbolID: Optional[str] = None):
    set = { "$set": {"allowUpdate" : True}}
    if symbolID:      
        query = {'symbolID': symbolID}
        result = dbSymbol.update_many(query, set)
    else:
        result = dbSymbol.update_many({}, set)
    return "Enable symbol Success"

@app.post('/disableSymbols', tags=["symbol"])
async def disable_symbol(symbolID: Optional[str] = None):
    set = { "$set": {"allowUpdate" : False}}
    if symbolID:      
        query = {'symbolID': symbolID}
        result = dbSymbol.update_many(query, set)
    else:
        result = dbSymbol.update_many({}, set)
    return "Disable symbol Success"

@app.delete('/unregisterSymbols', tags=["symbol"])
async def unregister_symbol(symbolID: Optional[str] = None):
    if symbolID:      
        query = {'symbolID': symbolID}  
        result = dbSymbol.delete_many(query)
    else:
        result = dbSymbol.delete_many({})
    return "Delete Success"