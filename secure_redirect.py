import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse

app = FastAPI()


@app.route('/{_:path}')
async def https_redirect(request: Request):
        return RedirectResponse(request.url.replace(scheme='https'))

if __name__ == '__main__':
        uvicorn.run('secure_redirect:app', port=80, host='127.0.0.1')
