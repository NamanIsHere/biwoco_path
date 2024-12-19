"""
This module provides functionality for saving validated movie data to a MongoDB collection.

It includes functionality for:
- Validating data using Pydantic models.
- Inserting data into a MongoDB collection.
- Logging messages and errors related to the operations.
"""
import os
from dotenv import load_dotenv
from logs import log
from utils import save_data
from config import db_config
from transform_validate import validate_data
from scrapers.movies_scraper import fetch_url, scrape_movies_from_each_country

if __name__ == '__main__':
    #load variables in .env file
    load_dotenv()
    base_url = os.getenv('base_url')
    get_collection = os.getenv('movie_collection')
    #1 Connect to MongoDB
    store_in_collection = db_config.DatabaseConfig.connect_to_database(get_collection)

    #2 extract data from webpage & then transform anc validate inside the method
    html_content = fetch_url(base_url)
    if html_content is None:
        log.log_message('failed to fetch the IMDB page.')
    scraped_data = scrape_movies_from_each_country(html_content)

    #3 transform and validate data
    validated_data = validate_data.validate_movies(scraped_data)

    #4 store to database
    if store_in_collection is not None and validated_data:
        save_data.save_data_to_db(validated_data, store_in_collection)
    else:
        MESSAGE = 'Opps! something went wrong at main function when\
        trying to store data into database!'
        log.log_message(MESSAGE)
