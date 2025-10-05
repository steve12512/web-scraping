from scrape_houses import House_Scraper


places_to_be_scraped = {
    'Amsterdam' : ['Amsterdam', 'Netherlands', 'https://housinganywhere.com/s/Amsterdam--Netherlands', 'nl'],
    'London' : ['London', 'UK', 'https://housinganywhere.com/s/London--United-Kingdom', 'gb']
}

for city, values in places_to_be_scraped.items():
    country = values[1]
    url = values[2]
    word_to_split_listing_id_on_the_url = values[3]
    
    scraper = House_Scraper(city,country,url,word_to_split_listing_id_on_the_url)
    scraper.scrape_pages_and_save_them()





# scraper = House_Scraper('Amsterdam','Netherlands','https://housinganywhere.com/s/Amsterdam--Netherlands', 'nl')

# scraper.scrape_pages_and_save_them()


