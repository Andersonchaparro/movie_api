from fastapi.routing import APIRouter
from typing import List, Optional
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
from config.database import Session


movie_router = APIRouter()


class Movies(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=5, max_length=15)
    overview: str = Field(min_length=15, max_length=50)
    year: int = Field(le=2022)
    rating: float = Field(ge=1.0, le=10.0)
    category: str =  Field(min_length=5, max_length=10)
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "Mi Pelicula",
                    "overview": "Descripcion de la pelicula",
                    "year": 2022,
                    "rating": 1.0,
                    "category": "Acción"
                }
            ]
        }
    }


@movie_router.get('/movies', tags=['movies'], response_model=List[Movies], 
         status_code=200, dependencies=[Depends(JWTBearer())])
def get_all_movies() -> List[Movies]:
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=result)

@movie_router.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)) -> Movies:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    
    if not result:
        return JSONResponse(status_code=404, content={'message':'Movie not found'})

    return JSONResponse(content=jsonable_encoder(result))

@movie_router.get('/movies/', tags=['movies'], response_model=List[Movies])
def get_movie_by_category(category: str = Query(min_length=5, 
                          max_length=15)) -> List[Movies]:
    
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.category==category).all()

    #movies_by_category = filter(lambda y: y['category'].lower() == category 
    #                            , movies)
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movies) -> dict:

    db_session = Session()
    new_movie = MovieModel(**movie.model_dump())
    db_session.add(new_movie)
    db_session.commit()

    return JSONResponse(status_code=201, content={'message': 'Movie added'})

@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movies) -> dict:

    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        return JSONResponse(status_code=404, content={'message':'Movie not found'})
    
    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category

    db.commit()
    
    return JSONResponse(status_code=200, content={'message': 'the movie has been modified'})

@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    
    if not result:
        return JSONResponse(status_code=404, content={'message':'Movie not found'})

    db.delete(result)
    db.commit()

    return JSONResponse(status_code=200, content={'message': 'Movie has been removed'})
