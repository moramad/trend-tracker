import json, pymongo
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

dbClient = pymongo.MongoClient("mongodb+srv://mo_user:resistor1watt@moramad-cluster.p88xu.mongodb.net/?retryWrites=true&w=majority")
db = "trendTracker"
dbSymbol = dbClient[db]["symbol"]
dbAccount = dbClient[db]["account"]
dbPortofolio = dbClient[db]["portofolio"]
dbTrend = dbClient[db]["trend"]

def Symbols(symbolID, symbolType, allowUpdate, tickerID):
    data = {
        'symbolID': symbolID,
        'symbolType': symbolType,
        'allowUpdate': allowUpdate,
        'tickerID': tickerID
    }
    return data

def Coins(id, currentPrice, dateTrans):
    data = {
        'id': id,
        'symbol': "",
        'name': "",
        'asset_platform_id': "-",
        'platforms': {},
        'categories': [],
        'contract_address': "-",
        'hashing_algorithm': "-",
        'market_cap_rank': "-",
        'coingecko_rank': "-",
        'market_data': {
            'current_price': {
                'usd': currentPrice,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'total_value_locked': {
                "btc": 0,
                "usd": 0
            },
            'mcap_to_tvl_ratio': 0,
            'fdv_to_tvl_ratio': 0,
            'ath': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'ath_change_percentage': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'ath_date': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'atl': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'atl_change_percentage': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'atl_date': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            market_cap: {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            fully_diluted_valuation: {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            total_volume: {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'high_24h': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'low_24h': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'price_change_24h': 0,
            'price_change_percentage_24h': 0,
            'price_change_percentage_7d': 0,
            'price_change_percentage_14d': 0,
            'price_change_percentage_30d': 0,
            'price_change_percentage_60d': 0,
            'price_change_percentage_200d': 0,
            'price_change_percentage_1y': 0,
            'market_cap_change_24h': 0,
            'market_cap_change_percentage_24h': 0,
            'price_change_24h_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'price_change_percentage_1h_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'price_change_percentage_24h_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'price_change_percentage_7d_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'price_change_percentage_14d_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'price_change_percentage_30d_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'price_change_percentage_60d_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'price_change_percentage_200d_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'price_change_percentage_1y_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'market_cap_change_24h_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'market_cap_change_percentage_24h_in_currency': {
                'usd': 0,
                'idr': 0,
                'btc': 0,
                'bnb': 0,
                'eth': 0
            },
            'total_supply': 0,
            'max_supply': 0,
            'circulating_supply': 0,
            'last_updated': 0
        }
    }
    return data

def Accounts(username, name, email, password, roles, active):
    data = {
        'username': username,
        'name': name,
        'email': email,
        'password': password,
        'roles': roles,
        'active': active
    }
    return data

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class Symbol(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    symbolID: str
    tickerID: str
    allowUpdate: bool
    symbolType: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "symbolID": "<example>",
                "tickerID": "<example>",
                "allowUpdate": True,
                "symbolType": "crypto/stock",
            }
        }

class Account(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id')
    username: str
    name: str
    email: str
    roles: str
    active: bool
    password: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "username": "<example>",
                "name": "<example>",
                "active": True,
                "email": "<example>",
                "roles": "reader/writer",
                "password": "<example>"
            }
        }

def main():
    print("main function")

if __name__ == "__main__":
    main()