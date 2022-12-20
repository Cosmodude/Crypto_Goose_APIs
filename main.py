import logging.config
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Request, Response, Depends, Header
from fastapi.responses import JSONResponse
from logs.logs_config import LOGGING_CONFIG
import logging
from db.db_conf import get_db
from fastapi.middleware.cors import CORSMiddleware
from schemas.request_schemas.Project_request import Postdata
from models.NFT_Project import Project 
from sqlalchemy.orm import Session
import jwt
from External_API.API_script import CoinMarketCap_API as CMC_API, OpenSea_API

load_dotenv()

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()
origins = ["*"]

@app.middleware('http')
def catch_exceptions_middleware(request: Request, call_next):
    try:
        return call_next(request)
    except Exception as e:
        logger.exception(e)
        return Response('Internal server error', status_code=500)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def secure(token):
    print(token)
    decoded_token = jwt.decode(token, 'secret', algorithms='HS256', verify=False)
    # this is often used on the client side to encode the user's email address or other properties
    return decoded_token

@app.post('/projects')
def post(request: Postdata, db:Session=Depends(get_db)):
    logger.info(f"{request}")
    add_substance = Project(**dict(request))
    db.add(add_substance)
    db.commit()
    return True

@app.get('/projects')
def get_all(db:Session=Depends(get_db)):
    response=db.query(Project).all()
    #print(CMC_API(str(response[0].earn_token_name)))
    for project in response:
        project.__dict__["floor_price_D"]=\
        float(project.floor_price)*\
        CMC_API(project.buy_token_name)\
        ["data"][0]["quote"]["USD"]["price"]
        project.__dict__["earn_rate_D"]=\
        float(project.earn_rate_ET)*\
        CMC_API(str(project.earn_token_name))\
        ["data"][0]["quote"]["USD"]["price"]
    return response
    

@app.get('/project')
def get_all(id: int, db:Session=Depends(get_db)):
    response= db.query(Project).filter(Project.id == id).first().__dict__
    ### Adding dollar prices
    response["floor_price_D"]=\
    float(response["floor_price"])*\
    CMC_API(response["buy_token_name"])\
    ["data"][0]["quote"]["USD"]["price"]
    response["earn_rate_D"]=\
    float(response["earn_rate_ET"])*\
    CMC_API(response["earn_token_name"])\
    ["data"][0]["quote"]["USD"]["price"]
    return response
# @app.post('/new_card')
# def new_card(request: CardRequest, db:Session=Depends(get_db), authorization: str = Header(None)):
#     try: 
#         user_data = secure(authorization)
#     except Exception as e:
#         return 'Not valid token'

#     request = dict(request)
#     card = Card(**request, user_id=user_data['user_id'])
#     db.add(card)
#     db.commit()
#     db.refresh(card)
#     return card
'''print(CMC_API("ICE")\
    ["data"][0]["quote"]["USD"]["price"])'''
#@app.post('/register')
# def register(request: UserRegister, db: Session=Depends(get_db)):
#     user = db.query(User).filter(User.login==request.login).first()
#     if user:
#         return {'error': 'user is already registred'}
#     obj: User = db.query(User).order_by(User.id.desc()).first()
#     id = obj.id + 1
#     encoded_jwt = jwt.encode({"login": request.login, 'password': request.password, 'user_id': id}, "secret", algorithm="HS256")
#     user = User(login=request.login, email=request.email, password=request.password, token=encoded_jwt)
    
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user

# @app.post('/login')
# def login(request: UserLogin, db: Session=Depends(get_db)):
#     user = db.query(User).filter(User.login==request.login,).first()
#     if not user:
#         return {'error': 'No such user'}
#     else:
#         return user

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8007, reload=True, debug=True)
