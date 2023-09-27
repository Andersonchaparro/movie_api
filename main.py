from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from jwt_manager import create_token
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.routers import movie_router

app = FastAPI()
app.title = "movie_API"
app.version = "0.0.1"
app.middleware(ErrorHandler)
app.include_router(movie_router)

Base.metadata.create_all(bind=engine)

class User(BaseModel):
    email: str = "admin@gmail.com"
    password: str = "admin"


movies = [
     {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Accion'    
    },
    {
		"id": 2,
		"title": "El Pianista",
		"overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
		"year": "2009",
		"rating": 7.8,
		"category": "Drama"
	}
]

@app.get('/', tags=['home'])
def message():
    return HTMLResponse('<h1>Hello World</h1>')

@app.post('/login', tags=['auth'])
def login(user: User):
    if user.email == 'admin@gmail.com' and user.password == 'admin':
        token: str = create_token(user.model_dump())
        return JSONResponse(status_code=200, content=token)



