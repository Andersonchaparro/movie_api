from fastapi.security import HTTPBearer
from fastapi import Request
from fastapi import HTTPException
from utils.jwt_manager import validate_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth =  await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != 'admin@gmail.com':
            raise HTTPException(status_code=403, detail="Invalid Credentials")