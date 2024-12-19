from logs import log
from pymongo import MongoClient

class Database_config:
    """
    Class for configuring and connecting to a MongoDB database.
    """

    @staticmethod   
    def connect_to_database(collection_name):
        """
        Connect to the specified collection in the MongoDB database.

        :param collection_name: Name of the collection to connect to.
        :return: MongoDB collection instance or None if connection fails.
        """
        MONGO_URI = 'mongodb+srv://myAtlasDBUser:myatlas-001@myatlasclusteredu.tlzhb.mongodb.net/'
        DATABASE_NAME = 'imbd_on_coming_movies'
        
        try:            
            client = MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            collection = db[collection_name]
            log.log_message(f'connected to database {db.name} - collection {collection.name} successfully!')
            return collection
        except Exception as e:
            message = f'Failed to connect to database {db.name}!'
            log.log_error(message, e)
            return None
    