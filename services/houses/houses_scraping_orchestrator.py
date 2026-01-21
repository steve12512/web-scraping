from services.houses.scrape_houses import House_Scraper
from typing import List, Dict
from api.houses.house_models import Housing_Listing_Request


class House_Scraping_Orchestrator:

    def __init__(self, request: Housing_Listing_Request):
        self.request = request

    def run(self):

        city = self.request.city
        country = self.request.country
        url = self.request.url
        word_to_split_listing_id_on_the_url = self.request.word_to_split_page
        max_listings_to_be_scraped = self.request.max_number_of_listings_to_be_scraped

        scraper = House_Scraper(
            country,
            city,
            url,
            word_to_split_listing_id_on_the_url,
            max_listings_to_be_scraped,
        )
        scraper.scrape_pages_and_save_them()
