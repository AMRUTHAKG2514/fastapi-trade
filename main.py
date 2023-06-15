from fastapi import FastAPI,Query
from pydantic import BaseModel, Field
from typing import List, Optional,Dict,Any,Union

from typing_extensions import Annotated
import csv
from datetime import datetime

app = FastAPI()

class TradingDetails(BaseModel):
    buy_sell_indicator: str = Field(..., description="Buy or sell indicator")
    price: float = Field(..., description="Price of the trade")
    quantity: int = Field(..., description="Quantity of the trade")

class Trade(BaseModel):
    trade_id: int = Field(..., description="Unique ID for the trade")
    trader: str = Field(..., description="Name of the trader")
    instrument_id: str = Field(..., description="Trading name of trading instrument")
    counter_party: str = Field(..., description="Name of the party traded with")
    asset_class:str=Field(...,description="Type of the trading instrument")
    instrument_name: str = Field(..., description="Name of the owner of the instrument")
    trade_datetime: datetime = Field(..., description="Date and time of the trade")
    trading_details: TradingDetails = Field(..., description="Trading details")

def trades():
    trades = []
    with open('DATABASE_main .csv', 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            new_table = list(row.values())

            trade = Trade(trade_id=new_table[0], trader=new_table[1], instrument_id=new_table[2], \
                      instrument_name=new_table[3], asset_class=new_table[4], counter_party=(new_table[5]), \
                      trading_details=TradingDetails(buy_sell_indicator=(new_table[6]), price=(new_table[7]),quantity=(new_table[8])), \
                      trade_datetime=(new_table[9]))

            trades.append(trade)

    return trades

result = trades()

@app.get("/TRADES")
async def trade_list():
    return result

@app.get("/TRADE/{trade_id}")
async def unique_trade_id(trade_id:int):
    return result[trade_id-1]


@app.get("/TRADES/{name}")
async def name_tradelist(name:str):
    data=[]
    datad= []
    for row in result:
        trade_id = row.trade_id
        i = int(trade_id) - 1

        if (row.counter_party == name.upper()):
            data.append(row.trade_id)
        elif (row.trader == name.upper()):
            data.append(row.trade_id)
        elif (row.instrument_id == name.upper()):
            data.append(row.trade_id)
        elif (row.instrument_name == name.upper()):
            data.append(row.trade_id)
    m=0
    for a in data:

        i=int(a)
        database = [result[i - 1]]
        datad.append(database)
        m+=1
        if (len(data) == (m)):
            return {name: datad}


@app.get("/TRADES/")
async def filters(assetClass:Optional[str]=None,
                  minPrice: float = 44.9 ,
                  maxPrice: float= 5840.33,
                  start : datetime= datetime.strptime("2010-11-20T10:11:30.300013Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
                  end: datetime = datetime.strptime("2022-11-11T12:45:30.400525Z", "%Y-%m-%dT%H:%M:%S.%fZ"),
                  tradeType: Optional[str] = None
                  , ):
    filtered_trades=[]
    if assetClass:
       for row in result:
           if assetClass.upper()==row.asset_class:
               filtered_trades.append(row)

       return {"assetClass":filtered_trades}

    if tradeType:
        for row in result:
            if tradeType.upper() == row.trading_details.buy_sell_indicator:
                filtered_trades.append(row)
        return {"tradeType": filtered_trades}

    if (minPrice==44.9and maxPrice==5840.33):
        return {"44.9<=trading_details.price<=5840.33"}

    if(start==datetime.strptime("2010-11-20T10:11:30.300013Z", "%Y-%m-%dT%H:%M:%S.%fZ") and \
            end==datetime.strptime("2022-11-11T12:45:30.400525Z", "%Y-%m-%dT%H:%M:%S.%fZ")):
        return{"2010-11-20T10:11:30.300013Z<=trade_datetime<=2022-11-11T12:45:30.400525Z"}
