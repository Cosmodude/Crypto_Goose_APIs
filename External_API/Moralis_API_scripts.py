from moralis import evm_api
from datetime import date

params1 = {
    "date": date.today(), 
    "chain": "eth", 
}
api_key = "cN7VRpzofUx8OaF0NwFxhgBV42k8lswlcEuyAntsVj5ATbqnRUqBfKASwiAg9tw0"
params = {
    "address": "0x0F5D2fB29fb7d3CFeE444a200298f468908cC942", 
    "chain": "eth", 
    "exchange": "", 
    "to_block": evm_api.block.get_date_to_block(
    api_key=api_key,
    params=params1,
    )["block"], 
}

result = evm_api.token.get_token_price(
    api_key=api_key,
    params=params,
)

print(result["usdPrice"])