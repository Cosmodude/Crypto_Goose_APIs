from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from datetime import datetime

class PostUser(BaseModel):
    name: str
    email:str
    feedback:str