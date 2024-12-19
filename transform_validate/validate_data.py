"""
This module provides functionality for validating raw movie data.
The script performs the following tasks:
1. Uses the Pydantic `Movie` schema to validate raw movie data.
2. Converts raw data into structured dictionaries that meet the schema requirements.
3. Logs errors for any data that fails validation.
4. Returns a list of validated movie data.
"""
from pydantic import ValidationError
from models import schemas
from logs import log

@staticmethod
def validate_movies(raw_data):
    """
    Validates a list of raw movie data using the Movie schema.

    :param raw_data: List of raw movie data dictionaries.
    :return: List of validated movie data as dictionaries.
    """
    movie_model = schemas.Movie
    validated_movies = []

    for item in raw_data:
        try:
            validated_movie = movie_model(
                release_date = item['release_date'],
                title = item['title'],
                tags = item['tags'],
                actors = item['actors'],
                country = item['country'],
                image_url = item['image_url']
            )
            validated_movies.append(validated_movie.dict())
        except ValidationError as e:
            message = 'Data validation error'
            log.log_error(message, e)

    log.log_message('Done the data validation step!')
    return validated_movies
