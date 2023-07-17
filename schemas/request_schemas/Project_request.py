from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime

class Postdata(BaseModel):
    id: int
    name: str
    image: str
    buy_token_name:str
    chain_name:str
    floor_price: float
    earn_token_name: str
    last_updated: datetime
    earn_rate_ET: float
    contract_address: str

