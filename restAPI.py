from fastapi import FastAPI
from bson.json_util import dumps, loads
from dataModels import *

app = FastAPI()

@app.get('/symbols')
async def list_symbols():
    symbols = []
    result = dbSymbol.find()
    # list_result = list(result)
    # json_data = dumps(list_result)
    # return json_data
    for symbol in result:        
        symbols.append(Symbol(**symbol))      
    return {'symbols': symbols}

@app.post('/symbols')
async def register_symbol(symbol: Symbol):
    if hasattr(symbol, 'id'):
        delattr(symbol, 'id')        
    ret = dbSymbol.insert_one(symbol.dict(by_alias=True))
    symbol.id = ret.inserted_id
    return {'symbol': symbol}