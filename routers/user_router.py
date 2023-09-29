from jwt_manager import create_token
from pydantic import BaseModel
from fastapi.routing import APIRouter
from fastapi.responses import JSONResponse

user_router = APIRouter()

class User(BaseModel):
    email: str = "admin@gmail.com"
    password: str = "admin"

@user_router.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)