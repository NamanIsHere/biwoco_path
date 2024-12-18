from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from bson.objectid import ObjectId
from config.db_config import Database_config
from models.schemas import Movie, MovieCreate, MovieResponse, MovieUpdate
collection = Database_config.connect_to_database('movies')

endPoints = APIRouter()

def document_to_movie(doc):
    print(f'Processing document: {doc}')
    print(f'Type of document: {type(doc)}')
    try:
        return MovieResponse(
            id=str(doc.get('_id')),
            release_date=doc.get('release_date'),
            title=doc.get('title'),
            tags=doc.get('tags'),
            actors=doc.get('actors'),
            country=doc.get('country'),
            image_url=doc.get('image_url')
        )
    except KeyError as e:
        print(f'Missing key inn document: {e}')
        raise HTTPException(status_code='500', detail='something went wrong in database!')

@endPoints.get('/')
def get_all_movies():
    try:
        results = collection.find()
        if not results:
            raise HTTPException(status_code=404, detail='Movie was not found!')
        
        movies_list = list(results)
        response = [document_to_movie(movie) for movie in movies_list]
        return response
    except Exception as e:
        print(f'Error occurred at get all function: {e}')
        raise HTTPException(status_code=500, detail='something went wrong')
    
@endPoints.get('/pagination')
def get_all_movies_pagination(page: int=1, limit: int=10):
    try:
        if page < 1 or limit < 1:
            raise HTTPException(status_code=400, detail='Page and limit must be positive integers.')
        skip = (page - 1) * limit
        results = collection.find().skip(skip).limit(limit)

        movies_list = list(results)
        if not movies_list:
            raise HTTPException(status_code=404, detail='No movie was found!')
        
        response = [document_to_movie(movie) for movie in movies_list]
        return {
            'page': page,
            'limit': limit,
            'total_movies': collection.count_documents({}),
            'movies': response
        }
    except Exception as e:
        print(f'Error occurred at pagination function: {e}')
        raise HTTPException(status_code=500, detail='something went wrong at pagination')

@endPoints.get('/region')
def get_movies_for_region(region='United States'):
    try:
        results = collection.find({'country': region})
        movies_list = list(results)
        response = [document_to_movie(movie) for movie in movies_list]
        return {
            'get_movies_from': region,
            'movies': response
        }
    except Exception as e:
        print(f'Sommething went wrong at get movie for region: {e}')
        raise HTTPException(status_code=500, detail='something went wrong at get region')

@endPoints.delete('/{movie_id}')
def delete_movie(movie_id: str):
    try:
        result = collection.delete_one({'_id': ObjectId(movie_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail='aint movies was found!')
        return{'message': 'movie deleted successfully'}
    except Exception as e:
        print(f'Something went wrong at delete_movie: {e}')
        raise HTTPException(status_code=500, detail='Something went wrong at delete movie!')