"""
This module provides functionality for saving validated movie data to a MongoDB collection.

It includes functionality for:
- Validating data using Pydantic models.
- Inserting data into a MongoDB collection.
- Logging messages and errors related to the operations.
"""
from pydantic import ValidationError
from logs import log


def save_data_to_db(validated_data, collection):
    """
    Store validated movies data into collection in MongoDB.

    :param validated_data: data that went through validation step and
    are ready to be inserted into MongoDB.
    :param collection: collection name that input data will be stored.
    """
    if validated_data is not None and collection.name == 'movies':
        try:
            if isinstance(validated_data, list) and isinstance(validated_data[0], dict):
                data_to_save = validated_data
            else:
                data_to_save = [movie.dict() for movie in validated_data]

            result = collection.insert_many(data_to_save)
            message = f'Data was successfully saved to MongoDB with IDs:\
                {result.inserted_ids}'
            log.log_message(message)
        except ValidationError as e:
            message = 'An error occurred while saving data to MongoDB!'
            log.log_error(message, e)
