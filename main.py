from logs import log
from utils import save_data
from config import db_config
from transform_validate import validate_data
from scrapers.movies_scraper import fetch_url, scrape_movies_from_each_country

if __name__ == '__main__':
    #1 Connect to MongoDB
    store_in_collection = db_config.Database_config.connect_to_database('movies')

    #2 extract data from webpage & then transform anc validate inside the method
    base_url = 'https://www.imdb.com/calendar/?region=AF&type=MOVIE&ref_=rlm'
    html_content = fetch_url(base_url)
    if html_content is None:
        log.log_message('failed to fetch the IMDB page.')
    scraped_data = scrape_movies_from_each_country(html_content)

    #3 transform and validate data
    validated_data = validate_data.Validate_data.validate_movies(scraped_data)

    #4 store to database
    if store_in_collection is not None and validated_data:
        save_data.Save_scraped_data.save_data_to_db(validated_data, store_in_collection)
    else:
        log.log_message('Opps! something went wrong at main function when trying to store data into database!')    