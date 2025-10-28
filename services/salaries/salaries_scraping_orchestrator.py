from services.salaries.scrape_salaries import Software_Engineer_Scraper
from typing import List, Dict
from database.software_engineer.models import *
from database.software_engineer.crud_functions import *


class Salaries_Scraping_Orchestrator:

    def __init__(
        self,
        dictionary_of_places_to_scrape: Dict,
        save_to_db: bool = True,
        max_listings_to_be_scraped: int = 2,
    ):
        self.dictionary_of_places_to_scrape = dictionary_of_places_to_scrape

    def run(self):
        for key, values in self.dictionary_of_places_to_scrape.items():
            country = values[0]
            city = values[1]
            country_url = values[2]
            max_listings_to_be_scraped = values[3]

            scraper = Software_Engineer_Scraper(
                country, city, country_url, max_listings_to_be_scraped
            )
            scraper.sign_in_levels_fyi(scraper.driver)
            scraper.enter_salaries_page()
            elements = scraper.scrape_pages_for_fyi(about_to_scrapesecond_page=False)
            print(elements[0])
            df = scraper.edit_listing_columns(elements)
            sql_models = convert_list_to_sql_model_and_return_a_list_of_models(df,country,city)
            add_listings_to_db(sql_models)
            print("1")


locations_to_scrape = {
    "London Area": [
        "UK",
        "London",
        "https://levels.fyi/t/software-engineer/locations/london-metro-area",
        1,
    ]
    # 'Paris Area': 'https://levels.fyi/t/software-engineer/locations/greater-paris-area',
    # 'Madrid Area' :'https://www.levels.fyi/t/software-engineer/locations/madrid-metropolitan-area',
    # 'Greater Glasgow Area' : 'https://www.levels.fyi/t/software-engineer/locations/greater-glasgow-area',
    # 'Vienna' : 'https://www.levels.fyi/t/software-engineer/locations/vienna-metropolitan-area',
    # 'Dublin' : 'https://www.levels.fyi/t/software-engineer/locations/greater-dublin-area',
    # 'Greater Cambridge' : 'https://www.levels.fyi/t/software-engineer/locations/greater-cambridge-area',
    # 'Tallin' : 'https://www.levels.fyi/t/software-engineer/locations/tallinn-metropolitan-area',
    #  'Greater Oslo' : 'https://www.levels.fyi/t/software-engineer/locations/greater-oslo-region',
    #  'Greater Barcelona Area' : 'https://www.levels.fyi/t/software-engineer/locations/greater-barcelona-area',
    #  'Greater Stockholm Area' : 'https://www.levels.fyi/t/software-engineer/locations/greater-stockholm',
    #  'Stuttgart Greater Area' : 'https://www.levels.fyi/t/software-engineer/locations/stuttgart-metro-region',
    #  'Warsaw' : 'https://www.levels.fyi/t/software-engineer/locations/warsaw-metropolitan-area',
    #  'Tricity' : 'https://www.levels.fyi/t/software-engineer/locations/tricity',
    #  'Greater Rhine-Main Area' : 'https://www.levels.fyi/t/software-engineer/locations/greater-rhine-main-area',
    # 'Germany' : 'https://www.levels.fyi/t/software-engineer/locations/germany',
    # 'Netherlands' : 'https://www.levels.fyi/t/software-engineer/locations/netherlands'
}

for k, v in locations_to_scrape.items():
    orchestrator = Salaries_Scraping_Orchestrator({"k": [v[0], v[1], v[2], v[3]]})
    orchestrator.run()
