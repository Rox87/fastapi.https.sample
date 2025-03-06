import uvicorn
import logging
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import RedirectResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="HTTPS Redirect Service",
    description="A service to redirect HTTP traffic to HTTPS",
    version="1.0.0"
)

@app.route('/{_:path}')
async def https_redirect(request: Request):
    logger.info(f'Redirecting request from {request.url} to HTTPS')
    try:
        https_url = request.url.replace(scheme='https')
        return RedirectResponse(https_url)
    except Exception as e:
        logger.error(f'Error during redirect: {str(e)}')
        raise

if __name__ == '__main__':
    logger.info('Starting HTTP to HTTPS redirect service on port 80')
    uvicorn.run('secure_redirect:app', port=80, host='127.0.0.1')
