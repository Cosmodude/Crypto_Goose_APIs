#!/usr/bin/python
from dotenv import load_dotenv
load_dotenv()
import os
import requests
import mysql.connector
from mysql.connector import errorcode
from datetime import datetime

mydb = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME')
    )
print(mydb)
table_name='nft_pr'

OpenSea_Url_Ending= {"Ice Poker":"decentral-games-ice",
                     "Stepn": "stepn",
                     "League of Kingdoms": "league-of-kingdoms",
                     "Thetan Arena": "thetan-hero-bnb"}
quering_all=(f"SELECT id, nft_floor_price, daily_earn_rate_ET, required_token_name, earn_token_name, nft_required, project_name  FROM {table_name}; ")
updating=(f"UPDATE {table_name} SET nft_floor_price_D= %s, daily_earn_rate_D= %s, min_investment= %s WHERE id=%s ;")
quering_name=(f"SELECT id, project_name FROM {table_name};")

def get_from_db(db, process):
    cursor=db.cursor()
    cursor.execute(process)
    response=cursor.fetchall()
    db.commit() 
    cursor.close()
    return response

def set_update_time(db):
    cursor=db.cursor()
    process=f"UPDATE {table_name} SET last_updated='{datetime.now().replace( microsecond=0)}' ;"
    cursor.execute ( process )
    db.commit() 
    cursor.close()
    return True

def insert_into_db(db,process,data):
    cursor=db.cursor()
    cursor.execute(process,data)
    db.commit() 
    cursor.close()
    return True

def CoinMarketCap_API(symbol):
    coinmarketcap_url ="https://pro-api.coinmarketcap.com/v2/tools/price-conversion"
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv('X-CMC_PRO_API_KEY') ,
            }
    parameters = { "amount": 1, "symbol": symbol, "convert" : "USD"}
    json= requests.get(coinmarketcap_url,params=parameters, headers=headers).json()
    return json

def OpenSea_API(project_name):
    Opensea_collections_url = "https://api.opensea.io/api/v1/collection/"
    json= requests.get(Opensea_collections_url+project_name).json()
    #print(json)
    return json

def main():
    db_response=get_from_db(mydb,quering_name)
    for row in db_response:
        if row[1] in OpenSea_Url_Ending.keys():
            nft_price= OpenSea_API(OpenSea_Url_Ending[row[1]])["collection"]["stats"]["floor_price"]
            cursor=mydb.cursor()
            cursor.execute(f"UPDATE {table_name} SET nft_floor_price ={ nft_price } WHERE id={row[0]};")
            mydb.commit() 
            cursor.close()

    db_response=get_from_db(mydb,quering_all)
    for row in db_response:
        if row[6] in OpenSea_Url_Ending.keys():
            row=list(row)
            row[3]="ETH"
            row=tuple(row)
        #getting token prices
        required_token=CoinMarketCap_API(row[3])
        earn_token=CoinMarketCap_API(row[4])
        #print(CMC_response)
        update_data=(
        #nft_floor_price_D
        float(row[1])*required_token["data"][0]["quote"]["USD"]["price"],\
        #daily_earn_rate_ET
        float(row[2])*earn_token["data"][0]["quote"]["USD"]["price"],\
        #min_investment
        float(row[1])*required_token["data"][0]["quote"]["USD"]["price"]*float(row[5])*1.1,\
        row[0]
        )
        insert_into_db(mydb,updating,update_data)
    set_update_time(mydb)


main()
print(datetime.now().replace(second=0, microsecond=0))
"""for row in get_from_db(mydb,quering):
    print(row)
print(type(get_from_db(mydb,quering)[0][5]))"""

