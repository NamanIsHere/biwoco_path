from pydantic import ValidationError
from models import schemas
from logs import log_message

class Validate_data:
    def validate_movies(raw_data):
        movie_model = schemas.Movie
        validated_movies = []
        for item in raw_data:
            try:
                validated_movie = movie_model(release_date=item['release_date'], title=item['title'], tags=item['tags'], actors=item['actors'], country=item['country'], image_url=item['image_url'])
                validated_movies.append(validated_movie.dict())
            except ValidationError as e:
                print(f'Validation error: {e}')
                log_message.log_message_to_file(f'Validation error: {e}')

        log_message.log_message_to_file('Done the data validation step!')
        return validated_movies