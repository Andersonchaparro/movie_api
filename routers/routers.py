from fastapi.routing import APIRouter
from typing import List
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from models.movie import Movie as MovieModel
from middlewares.jwt_bearer import JWTBearer
from config.database import Session
from services.movies import MovieService
from schemas.movie import Movies


movie_router = APIRouter()


@movie_router.get('/movies', tags=['movies'], response_model=List[Movies], 
         status_code=200, dependencies=[Depends(JWTBearer())])
def get_all_movies() -> List[Movies]:
    db = Session()
    result = MovieService(db).get_movies()
    return JSONResponse(status_code=200, content=result)


@movie_router.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)) -> Movies:
    db = Session()
    result = MovieService(db).get_movie(id)

    if not result:
        return JSONResponse(status_code=404, content={'message':'Movie not found'})

    return JSONResponse(content=jsonable_encoder(result))


@movie_router.get('/movies/', tags=['movies'], response_model=List[Movies])
def get_movie_by_category(category: str = Query(min_length=5, 
                          max_length=15)) -> List[Movies]:
    
    db = Session()
    result = MovieService(db).get_movie_by_category(category)

    #movies_by_category = filter(lambda y: y['category'].lower() == category 
    #                            , movies)
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.post('/movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie(movie: Movies) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)

    return JSONResponse(status_code=201, content={'message': 'Movie added'})


@movie_router.put('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie(id: int, movie: Movies) -> dict:

    db = Session()
    result = MovieService.get_movie(id=id)

    if not result:
        return JSONResponse(status_code=404, content={'message':'Movie not found'})
    
    MovieService(db=db).update_movie(id, data=movie)
    
    return JSONResponse(status_code=200, content={'message': 'the movie has been modified'})


@movie_router.delete('/movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie(id: int) -> dict:
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id==id).first()
    
    if not result:
        return JSONResponse(status_code=404, content={'message':'Movie not found'})
    
    MovieService.delete_movie(id)

    db.commit()

    return JSONResponse(status_code=200, content={'message': 'Movie has been removed'})
