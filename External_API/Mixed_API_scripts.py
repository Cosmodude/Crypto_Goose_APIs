from dotenv import load_dotenv
load_dotenv()
import os
import requests

ice_poker_url ="https://api.opensea.io/api/v1/collection/decentral-games-ice"



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


OpenSea_API("stepn")
'''
print(axie_json["collection"]["stats"]["floor_price"])
print(axie_json["collection"]["primary_asset_contracts"][0]["address"])'''
#print(CoinMarketCap_API("ICE")["data"][0]["quote"]["USD"]["price"])
#Ice_poker_json=OpenSea_API(ice_poker_url)

"""BTC_json= CoinMarketCap_API(coinmarketcap_url, "ICE")
print(BTC_json["data"][0]["quote"]["USD"]["price"])
print(BTC_json)
print(Ice_poker_json["collection"]["stats"]["floor_price"])
print(Ice_poker_json["collection"]["primary_asset_contracts"][0]["address"])
print(Ice_poker_json["collection"]["image_url"])
print(Ice_poker_json["collection"]["telegram_url"])
print("https://twitter.com/"+Ice_poker_json["collection"]["twitter_username"])
print(Ice_poker_json["collection"]["discord_url"])"""


