from services.houses.scrape_houses import House_Scraper


places_to_be_scraped = {
    'Stockholm' : ['Stockholm', 'Sweden', 'https://housinganywhere.com/s/Stockholm--Sweden', 'se',1000],
    'Barcelona' : ['Barcelona', 'Spain', 'https://housinganywhere.com/s/Barcelona--Spain','es',1000],
    'London' : ['London', 'UK', 'https://housinganywhere.com/s/London--United-Kingdom', 'gb',1000],
    'Amsterdam' : ['Amsterdam', 'Netherlands', 'https://housinganywhere.com/s/Amsterdam--Netherlands', 'nl',1000],
}

for city, values in places_to_be_scraped.items():
    country = values[1]
    url = values[2]
    word_to_split_listing_id_on_the_url = values[3]
    
    scraper = House_Scraper(country,city,url,word_to_split_listing_id_on_the_url,1000)
    scraper.scrape_pages_and_save_them()
        #net start MongoDB




# scraper = House_Scraper('Amsterdam','Netherlands','https://housinganywhere.com/s/Amsterdam--Netherlands', 'nl')

# scraper.scrape_pages_and_save_them()


