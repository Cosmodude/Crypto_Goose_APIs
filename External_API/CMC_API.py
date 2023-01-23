from dotenv import load_dotenv
load_dotenv()
import os
import requests
import mysql.connector
from mysql.connector import errorcode

mydb = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME')
    )
print(mydb)
table_name='nft_pr'

quering=(f"SELECT id, nft_floor_price, daily_earn_rate_ET, required_token_name, earn_token_name, nft_required  FROM {table_name}; ")
updating=("UPDATE nft_pr SET nft_floor_price_D= %s, daily_earn_rate_D= %s, min_investment= %s WHERE id=%s ;")

def get_from_db(db, process):
    cursor=db.cursor()
    cursor.execute(process)
    response=cursor.fetchall()
    db.commit() 
    cursor.close()
    return response

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

def main():
    db_response=get_from_db(mydb,quering)
    for row in db_response:
        required_token=CoinMarketCap_API(row[3])
        earn_token=CoinMarketCap_API(row[4])
        #print(CMC_response)
        update_data=(\
        #table_name,\
        float(row[1])*required_token["data"][0]["quote"]["USD"]["price"],\
        float(row[2])*earn_token["data"][0]["quote"]["USD"]["price"],\
        float(row[1])*required_token["data"][0]["quote"]["USD"]["price"]*float(row[5])*1.1,\
        row[0]
        )
        insert_into_db(mydb,updating,update_data)


main()
print(table_name)
for row in get_from_db(mydb,quering):
    print(row)
print(type(get_from_db(mydb,quering)[0][5]))

