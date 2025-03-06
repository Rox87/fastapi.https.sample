import uvicorn
import subprocess
import json
import logging

from datetime import datetime
from typing import Union, List, Optional

from fastapi import FastAPI, Request, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class User(BaseModel):
    id: int
    name: str = Field(default="John Doe")
    signup_ts: Optional[datetime] = None
    friends: List[int] = []

    @validator('friends')
    def validate_friends(cls, v):
        if not all(isinstance(friend, int) for friend in v):
            raise ValueError('All friend IDs must be integers')
        return v

app = FastAPI(
    title="FastAPI HTTPS Sample",
    description="A sample FastAPI application with HTTPS support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    logger = logging.getLogger(__name__)
    
    # Log request details
    logger.info(f'Request headers: {dict(request.headers.items())}')
    logger.info(f'Query parameters: {dict(request.query_params.items())}')
    
    try:
        req = await request.json()
        logger.info(f'Request JSON: {req}')
        
        # Validate required fields
        if 'queryResult' not in req:
            raise HTTPException(status_code=400, detail="Missing 'queryResult' in request")
            
        query_result = req['queryResult']
        if 'parameters' not in query_result or 'name' not in query_result['parameters']:
            raise HTTPException(status_code=400, detail="Missing required parameters")
            
        name = query_result['parameters']['name']
        return {'fulfillmentText': f"Olá {name}"}
        
    except json.JSONDecodeError as e:
        logger.error(f'JSON decode error: {str(e)}')
        body = await request.body()
        logger.info(f'Request body: {body}')
        return JSONResponse(
            status_code=400,
            content={'error': 'Invalid JSON payload'}
        )
        
    except HTTPException as he:
        raise he
        
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        return JSONResponse(
            status_code=500,
            content={'error': 'Internal server error'}
        )
                 
if __name__ == '__main__':
        subprocess.Popen(['python', '-m', 'secure_redirect'])  # Add this
        uvicorn.run(
           'main:app', port=443, host='127.0.0.1',
           reload=True,
           ssl_keyfile='certs/key.pem',
           ssl_certfile='certs/cert.pem'
           )
