import requests
from parsel import Selector
from time import sleep
import random

from logs import log_message

#create session to maintain cookies and headers
session = requests.session()
session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",  # Pretend to came from Google
    "Connection": "keep-alive"
})

"""
This method is used to fetch data from the webpage.
Add session to fetch content from webpage.
"""
def fetch_url(url):
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        log_message.log_message_to_file(f'successfully fetched data on URL: {url}')
        return response.text
    except requests.exceptions.RequestException as e:
        log_message.log_message_to_file(f'Failed to fetch {url}: {e}')
        return None

"""
This method is used to get out the list of region on the webpage then be inserted into the scrape_movies_from_each_country
method to filter data.
"""
def get_country(html):
    selector = Selector(html)
    countries = []

    options = selector.css('select#country-selector option')
    
    for option in options:
        country_code = option.css('::attr(value)').get()
        country_name = option.css('::text').get()
        countries.append({'country_code': country_code, 'country_name': country_name})
    return countries

"""
This method is used to scrape out the movie data that show on the page.
"""
def scrape_movies(html, region):
    selector = Selector(html)
    sections = selector.css("article[data-testid='calendar-section']")
    movies=[]
    if sections != []:
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
                    log_message.log_message_to_file(message_to_log)
                    print(message_to_log)
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

"""
On the top of the IMDB webpage there is a list of option for countries.
This method is created to scrape the movies filtered by each country.
"""
def scrape_movies_from_each_country(html):
    movies_list = []
    for country in get_country(html):
        country_code = country['country_code']
        country_name = country['country_name']
        fixed_url = f"https://www.imdb.com/calendar/?region={country_code}&type=MOVIE&ref_=rlm"
        sleep(random.uniform(2, 5)) #use delay time to avoid detection
        log_message.log_message_to_file(f'now fetching from region: {country_name}...')
        print(f'now fetching from region: {country_name}...')
        html_content = fetch_url(fixed_url)
        movies_list.extend(scrape_movies(html_content, country_name))

        message_to_log = f"""
        =======================
        {len(movies_list)}
        \n
        """
        log_message.log_message_to_file(message_to_log)
        print(message_to_log)
        if not html_content:
            log_message.log_message_to_file(f'In function scrape_movies_from_each_country failed to fetched data for region: {country['country_name']}')
            return []
    
    return movies_list