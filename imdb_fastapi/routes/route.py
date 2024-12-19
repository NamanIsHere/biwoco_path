"""
Module: Fast API Route

This module defines API Routes with CRUD methods.
get_all_movies is used to fetch all movies data in database.
get_all_movies_pagination is used to fetch all movies but with pagination.
get_movies_for_region is used to fetch movies by region.
delete_movie is used to delete movie by it _id.
"""
import os
from dotenv import load_dotenv
from bson.objectid import ObjectId
from fastapi import APIRouter, HTTPException
from config.db_config import DatabaseConfig
from models.schemas import MovieResponse
from logs import log

#load variables in .evn file
load_dotenv()
# Connect to the 'movies' collection in MongoDB
db_collection = os.getenv('movie_collection')
collection = DatabaseConfig.connect_to_database(db_collection)

#Define API Router for movie endpoints
endPoints = APIRouter()

def document_to_movie(doc):
    """
    Converts a MongoDB document to a MovieResponse object.

    :param doc: MongoDB document.
    :return: MovieResponse object.
    """
    message = f'Type of document: {type(doc)}'
    log.log_debug(message)
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
        message = 'Missing key in document!'
        log.log_error(message, e)
        raise HTTPException(status_code=500, detail='something went wrong!\
                            missing key in document.') from e
@endPoints.get('/')
def get_all_movies():
    """
    Fetch all movies from the database.

    :return: List of MovieResponse objects.
    """
    message = 'Fetching all movies'
    log.log_debug(message)
    try:
        results = collection.find()
        if not results:
            message = 'No movies found!'
            log.log_warning(message)
            raise HTTPException(status_code=404, detail='No movies found!')

        movies_list = list(results)
        response = [document_to_movie(movie) for movie in movies_list]
        return {
            'Total movies: ':len(response),
            'Movies list: ': response
        }
    except Exception as e:
        message = 'Error occurred at get all movies function! '
        log.log_error(message, e)
        raise HTTPException(status_code=500, detail='something went wrong') from e

@endPoints.get('/pagination')
def get_all_movies_pagination(page: int=1, limit: int=10):
    """
    Fetch movies with pagination.

    :param page: Page number.
    :param limit: Number of movies per page.
    :return: Paginated movies response.
    """
    message = f'Fetching movies with pagination: page={page}, limit={limit}'
    log.log_debug(message)
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
        raise HTTPException(status_code=500, detail='something went wrong at pagination') from e

@endPoints.get('/region')
def get_movies_for_region(region='United States'):
    """
    Fetch movies for a specific region.

    :param region: Region name.
    :return: Movies from the specified region.
    """
    message = f'Fetching movies for region: {region}'
    log.log_debug(message)
    try:
        results = collection.find({'country': region})
        movies_list = list(results)
        response = [document_to_movie(movie) for movie in movies_list]
        return {
            'get_movies_from': region,
            'movies': response
        }
    except Exception as e:
        message = 'Something went wrong in get_movies_for_region! '
        log.log_error(message, e)
        raise HTTPException(status_code=500, detail='something went wrong at get region') from e

@endPoints.delete('/{movie_id}')
def delete_movie(movie_id: str):
    """
    Delete a movie by its ID.

    :param movie_id: ID of the movie to delete.
    :return: Success message if the movie is deleted.
    """
    message = f'Deleting movie with ID: {movie_id}'
    log.log_debug(message)
    try:
        result = collection.delete_one({'_id': ObjectId(movie_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail='aint movies was found!')
        return{'message': 'movie deleted successfully'}
    except Exception as e:
        message = 'Something went wrong at delete_movie! '
        log.log_error(message, e)
        raise HTTPException(status_code=500, detail='Something went wrong\
        at delete movie!') from e
