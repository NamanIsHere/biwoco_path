"""
Module: Connect to MongoDB Database

This module defines methods to connect to MongoDB.
One already have database name in it and just need collection name as method input data.
One require for both database name and collection name as input data for various purpose of uses.
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from logs import log

# Load environment variables from the .env file
load_dotenv()

class DatabaseConfig:
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
        mongo_uri = os.getenv('MONGO_URI')
        database_name = os.getenv('database')
        try:
            client = MongoClient(mongo_uri)
            db = client[database_name]
            collection = db[collection_name]
            message = f'connected to database {db.name} -\
            collection {collection_name} successfully!'
            log.log_message(message)
            return collection
        except ConnectionError as e:
            message = f'Failed to connect to database {db.name}!'
            log.log_error(message, e)
            return None

    @staticmethod
    def connect_database(database_name, collection_name):
        """
        Connect to specified database and collection in MongoDB database.

        :param database_name: Name of database to connect.
        :param collection_name: Name of collection to connect.
        :return: MongoDB collection instance or None if connection fails.
        """
        mongo_uri = os.getenv('MONGO_URI')
        try:
            client = MongoClient(mongo_uri)
            db = client[database_name]
            collection = db[collection_name]
            message = f'connected to database {db.name} -\
            collection {collection.name} successfully!'
            log.log_message(message)
            return collection
        except ConnectionError as e:
            message = f'Failed to connect to database {db.name}!'
            log.log_error(message, e)
            return None
