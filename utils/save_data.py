from pymongo import MongoClient
from logs import log_message

class Save_scraped_data:
    def save_data_to_db(validated_data, collection):
        if validated_data is not None and collection.name == 'movies':
            print(type(validated_data))

            try:
                if isinstance(validated_data, list) and isinstance(validated_data[0], dict):
                    data_to_save = validated_data
                else:
                    data_to_save = [movie.dict() for movie in validated_data]

                result = collection.insert_many(data_to_save)
                log_message.log_message_to_file(f'Data was successfully saved to MongoDB with IDs: {result.inserted_ids}')
            except Exception as e:
                log_message.log_message_to_file(f'An error occurred while saving data to MongoDB: {e}')
        