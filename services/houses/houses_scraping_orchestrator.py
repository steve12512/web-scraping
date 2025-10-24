from services.houses.scrape_houses import House_Scraper
from typing import List, Dict


class House_Scraping_Orchestrator:

    def __init__(self, dictionary_of_places_to_scrape: Dict):
        self.dictionary_of_places_to_scrape = dictionary_of_places_to_scrape

    def run(self):
        for city, values in self.dictionary_of_places_to_scrape.items():
            country = values[1]
            url = values[2]
            word_to_split_listing_id_on_the_url = values[3]
            max_listings_to_be_scraped = values[4]
            scraper = House_Scraper(
                country,
                city,
                url,
                word_to_split_listing_id_on_the_url,
                max_listings_to_be_scraped,
            )
            scraper.scrape_pages_and_save_them()
