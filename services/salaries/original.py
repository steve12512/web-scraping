# %%
import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pprint
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC


import os
import json

import sys
sys.path.append('/full/path/to/web-scraping')



from salaries_functions import create_country_file, write_jobs_to_txt, scrape_pages, parse_response_to_csv, get_netherlands_url, get_dataframe, convert_cols_to_float

os.chdir('../database')
from crud_functions import write_dataframes_to_db
from models import Software_Engineer

os.chdir('../salaries')

# %%
netherlands_url = get_netherlands_url()
response = requests.get(netherlands_url)

# %%
germany_url = 'https://techpays.com/europe/germany'
response = requests.get(germany_url)

# %%
netherlands_url = 'https://techpays.com/europe/netherlands'
response = requests.get(netherlands_url)
create_country_file('netherlands')
create_country_file('germany')

# %%
scrape_pages(netherlands_url)
scrape_pages(germany_url)

# %% [markdown]
# earlier netherlands iteration crashed at 129th iteration
# 
# berlin search has to stop at the 107th iteration! (added break statement)

# %%
parse_response_to_csv('berlin')
parse_response_to_csv('netherlands')

# %%
for title in dutch_salaries['title'].dropna().unique():
    if 'senior' in title:
        print(title)
    if 'medior' in title:
        print(title)
    if 'junior' in title:
        print(title)

# %%

def get_page_filter_button_types_dict():
    arguments = dict.fromkeys(('locationFilterButton','jobFamilyFilterButton', 'seniorityFilterButton','roleTypeFilterButton','companyFilterButton'))
    return arguments


def get_filter_button_values(driver, filter_button):
    '''
    This functions receives a WebDriver object and a button id Object
    It returns a dictionary of all possible values for that button.
    '''
    options = {}
    button_class = re.sub(r'Button', '', filter_button) + 'Options'
    print(f'Filter button is {filter_button}, and button class is {button_class}')

    button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, filter_button))
    )
    
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    
    
    
    button.click()


    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, button_class))
    )

    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    dropdown = soup.find("div", id= button_class)
    locations = dropdown.find_all("a")

    for loc in locations:
        name = loc.text.strip()
        link = "https://techpays.com" + loc["href"]
        #print(f"{name}: {link}")
        options[name] = link
    button.send_keys(Keys.SPACE)
    return options





#########   MAIN    ####
driver = webdriver.Chrome()
driver.get(netherlands_url)
button_ids = get_page_filter_button_types_dict()
button_id_values = {button_id: {} for button_id in button_ids}

for button_id in button_ids:
    button_id_values = get_filter_button_values(driver, button_id)
    button_ids[button_id] = button_id_values
    print(button_ids[button_id])

    
    
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
    driver.execute_script("document.querySelector('body').click();")
    time.sleep(1) 




# %%
print(json.dumps({button_id: button_ids[button_id]}, indent=2, ensure_ascii=False))


# %%
from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def read_root():
    return 'Hello World'

# %%

os.chdir('../database')
from models import software_engineer

os.chdir('../salaries')

-
from models import software_engineer


# %%
os.chdir('../salaries')

# %%

os.chdir('../database')
from crud_functions import write_dataframes_to_db
from models import software_engineer

# %%
df = get_dataframe('berlin')
df = convert_cols_to_float(df)
df['country'] = 'Germany'

write_dataframes_to_db(df, Software_Engineer)

# %%
x = get_dataframe('Netherlands')
x['country'] = 'The Netherlands'

write_dataframes_to_db(x, Software_Engineer)

# %%
germany_from_fyi = scrape_from_fyi('Germany')

# %%



