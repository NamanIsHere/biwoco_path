"""
Scraping Module.
This module provide methods for scraping data.
"""

import os
import random
from time import sleep
from dotenv import load_dotenv
import requests
from parsel import Selector
from logs import log

#load variables in .env file
load_dotenv()
#create session to maintain cookies and headers
session = requests.session()
session_headers = {
    "User-Agent": os.getenv("user-agent"),
    "Accept-Language": os.getenv("accept-language"),
    "Accept-Encoding": os.getenv("accept-encoding"),
    "Referer": os.getenv("referer"),
    "Connection": os.getenv("connection"),
}
session.headers.update(session_headers)

def fetch_url(url):
    """
    Fetches content from the specified URL using the session.

    :param url: The URL to fetch data from.
    :return: HTML content as text if successful, None otherwise.
    """
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        log.log_message(f'successfully fetched data from URL: {url}')
        return response.text
    except requests.exceptions.RequestException as e:
        message = f'Failed to fetch {url}'
        log.log_error(message, e)
        return None

def get_country(html):
    """
    Extracts a list of countries from the webpage content.

    :param html: HTML content of the webpage.
    :return: List of dictionaries containing country codes and names.
    """
    selector = Selector(html)
    countries = []

    options = selector.css('select#country-selector option')

    for option in options:
        country_code = option.css('::attr(value)').get()
        country_name = option.css('::text').get()
        countries.append({'country_code': country_code, 'country_name': country_name})

        log.log_message(country_code)

    return countries

def scrape_movies(html, region):
    """
    Scrapes movie data from the provided HTML content for a given region.
    Check if there are any movies data on the page. if none append the 
    default values to movies list.

    :param html: HTML content of the webpage.
    :param region: The name of the region for the movies.
    :return: List of dictionaries containing movie details.
    """
    selector = Selector(html)
    sections = selector.css("article[data-testid='calendar-section']")
    movies = []

    if sections:
        for section in sections:
            release_date = section.css("div[data-testid='release-date'] h3::text").get()
            movie_items = section.css("li[data-testid='coming-soon-entry']")

            for item in movie_items:
                title = item.css('a::text').get()
                list_tags = item.css('ul.ipc-metadata-list-summary-item__tl span::text').getall()
                list_actors = item.css('ul.ipc-metadata-list-summary-item__stl span::text').getall()
                image_url = item.css('img::attr(src)').get()

                if image_url is None:
                    image_url = 'N/A'
                    message_to_log = f"""
                    **************************
                    Movie name {title} in {region} do not have any images!\n
                    """
                    log.log_message(message_to_log)

            movies.append({
                'release_date': release_date,
                'title': title,
                'tags': list_tags,
                'actors': list_actors,
                'country': region,
                'image_url': image_url
            })
    else:
        movies.append({
            'release_date': 'Jan 01, 2001',
            'title': 'Unknown title',
            'tags': [],
            'actors': [],
            'country': region,
            'image_url': 'N/A'
        })
    return movies

def scrape_movies_from_each_country(html):
    """
    Scrapes movie data for each country listed on the webpage.

    :param html: HTML content of the initial webpage.
    :return: Combined list of movies from all countries.
    """
    movies_list = []
    countries = get_country(html)

    for country in countries:
        country_code = country['country_code']
        country_name = country['country_name']
        fixed_url = f"https://www.imdb.com/calendar/?region={country_code}&type=MOVIE&ref_=rlm"
        sleep_time = random.uniform(2, 5)
        sleep(sleep_time)#use delay time to avoid detection
        log.log_message(f'fetching from region: {country_name} on {sleep_time}...')

        html_content = fetch_url(fixed_url)
        if not html_content:
            message = f'In function crape_movies_from_each_country\
              failed to fetched data for region: {country['country_name']}'
            log.log_message(message)
            return []
        movies_list.extend(scrape_movies(html_content, country_name))

        message_to_log = f"""
        =======================
        {len(movies_list)}
        \n
        """
        log.log_message(message_to_log)

    return movies_list
