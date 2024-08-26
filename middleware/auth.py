from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from passlib.context import CryptContext
from db.database import get_database
import logging

app = FastAPI()

logging.basicConfig(
    filename='system_audit.log', 
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger("BasicAuthMiddleware")

pwd_context = CryptContext(schemes=["bcrypt", "pbkdf2_sha256"], deprecated="auto")

security = HTTPBasic()

class BasicAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, db):
        super().__init__(app)
        self.db = db

    async def dispatch(self, request: Request, call_next):
        logger.info(f"Request received: {request.method} {request.url.path}")
        
        credentials = None  

        if request.url.path not in ["/login", "/open-endpoint"]:
            try:
                credentials = await security(request)
                if not self.authenticate_user(credentials):
                    logger.warning(f"Authentication failed for user: {credentials.username}")
                    raise HTTPException(status_code=401, detail="Invalid username or password")
                logger.info(f"User {credentials.username} authenticated successfully")
            except HTTPException as exc:
                if credentials:
                    logger.error(f"Authentication error: {exc.detail} for user: {credentials.username}")
                else:
                    logger.error(f"Authentication error: {exc.detail} - No credentials provided")
                response = Response(content=str(exc.detail), status_code=exc.status_code)
                response.headers["WWW-Authenticate"] = "Basic"
                return response
        
        response = await call_next(request)
        logger.info(f"Request processed: {request.method} {request.url.path} with status {response.status_code}")
        return response

    def authenticate_user(self, credentials: HTTPBasicCredentials):
        db = self.db
        users = db['users']
        user = users.find_one({"username": credentials.username})
        if user and pwd_context.verify(credentials.password, user['password_hash']):
            return True
        return False

app.add_middleware(BasicAuthMiddleware, db=get_database())
