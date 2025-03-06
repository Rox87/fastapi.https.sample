import uvicorn
import subprocess
import json

from datetime import datetime
from typing import Union

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field

from typing import List, Optional


class User(BaseModel):
    id: int 
    name:str = Field(name='John Doe')
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

app = FastAPI()

@app.get("/")
def main():
    return {"GOD":True}

def hook(name:str="Heloani"):

    usuario_atual = { 'id':123,
                'name':name,
                'signup_ts': datetime.now(),
                'friends': [1, 2, '3'],
                }
    user = User(**usuario_atual)
    return {'fulfillmentText': f'user:{user.dict()}'}

@app.post("/dummy")
async def get_body(request: Request):
    return await request.body()

@app.post("/dummy2")
async def get_json(request: Request):
    return await request.json()

@app.get("/webhook")
def get_hook(name:str="Heloani"):
    return hook(name)

@app.post("/webhook")
async def post_hook(request: Request):    
    print(f'request header       : {dict(request.headers.items())}' )
    print(f'request query params : {dict(request.query_params.items())}')  
    try :
        req = await request.json()
        print(f'request json         : {req}')
    except Exception as err:
        # could not parse json
        req = await request.body()
        print(f'request body         : {req}')
    try:
        return {'fulfillmentText': f"Olá {req['queryResult']['parameters']['name']}"}
    except:
        return {'fulfillmentText': f"{req}"}
                 
if __name__ == '__main__':
        subprocess.Popen(['python', '-m', 'https_redirect'])  # Add this
        uvicorn.run(
           'main:app', port=443, host='127.0.0.1',
           reload=True
           #,ssl_keyfile='/etc/letsencrypt/live/flyson.com.br/privkey.pem',
           #ssl_certfile='/etc/letsencrypt/live/flyson.com.br/fullchain.pem'
           )
