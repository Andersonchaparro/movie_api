from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from config.database import engine, Base
from middlewares.error_handler import ErrorHandler
from routers.routers import movie_router
from routers.user_router import user_router

app = FastAPI()
app.title = "movie_API"
app.version = "0.0.1"
app.middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


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
