from pymongo import MongoClient
from logs import log_message

class Database_config:
    
    def connect_to_database(collection):
        try:
            MONGO_URI = 'mongodb+srv://myAtlasDBUser:myatlas-001@myatlasclusteredu.tlzhb.mongodb.net/'
            database = 'imbd_on_coming_movies'
            client = MongoClient(MONGO_URI)
            db = client[database]
            request_collection = db[collection]
            log_message.log_message_to_file(f'connected to database {db.name} - {request_collection.name} successfully!')
            return request_collection
        except Exception as e:
            log_message.log_message_to_file(f'Opps!! something went wrong when trying to connect to database {db.name}: {e}')
            return None
    