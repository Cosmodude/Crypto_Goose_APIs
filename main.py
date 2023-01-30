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
from schemas.request_schemas.User_pre_request import PostUser
from models.NFT_Project import Projects,Project
from models.User_pre import User
from sqlalchemy.orm import Session
import jwt
from External_API.API_scripts import CoinMarketCap_API as CMC_API, OpenSea_API
from  External_API.Mailing_scripts import send_email
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from datetime import datetime

load_dotenv()

Not_on_Opensea={"Axie Infinity", "Thetan Arena", "Mobox","Gods Unchained",}
OpenSea_Url_Ending= {"Ice Poker":"decentral-games-ice","Stepn": "stepn","League of Kingdoms": "league-of-kingdoms" }

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

app = FastAPI()
origins = [
    "https://www.crypto-goose.com/:1",
    "211.219.144.185", "92.38.148.40",
    "https://www.crypto-goose.com/",
    ]
origins =["*"]



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
    allow_methods=["GET","POST"],
    allow_headers=["Content-Type",],
    )
'''
    HTTPSRedirectMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)
''' 

def secure(token):
    print(token)
    decoded_token = jwt.decode(token, 'secret', algorithms='HS256', verify=False)
    # this is often used on the client side to encode the user's email address or other properties
    return decoded_token


@app.get('/projects')
def get_all(db:Session=Depends(get_db)):
    response=db.query(Projects).all() 
    return response
    

@app.get('/project')
def get_all(id: int, db:Session=Depends(get_db)):
    project= db.query(Project).filter(Project.id == id).first()
    project.category=str(project.category).split(", ")
    return project

@app.post('/user_pre')
def post_user(request: PostUser, db:Session=Depends(get_db)):
    add_substance = User(**dict(request))
    add_substance.entry_time=datetime.datetime
    db.add(add_substance)
    db.commit()
    send_email(request.email, request.name)
    return True, request

@app.get('/user_pre')
def get_user(id: int, db:Session=Depends(get_db)):
    response= db.query(User).filter(User.id == id).first().__dict__
    return response

@app.get('/users_pre')
def get_users(db:Session=Depends(get_db)):
    response= db.query(User).all()
    return response

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


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8007, reload=True, debug=True)
