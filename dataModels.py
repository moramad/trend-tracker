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

def main():
    print("main function")

if __name__ == "__main__":
    main()