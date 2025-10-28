from salaries_functions import *
import requests
import pprint
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os

from dotenv import load_dotenv


os.chdir("C:/Users/steve/web-scraping/database")

from crud_functions import write_dataframes_to_db, df_to_sql
from models import software_engineer_salaries
from sqlalchemy import Engine

salaries_url = "https://www.levels.fyi/t/software-engineer/locations/germany"
driver = webdriver.Chrome()
sign_in_levels_fyi(driver)
driver.get(salaries_url)


driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(2)
data = scrape_pages_for_lyi(driver)
len(data)


df = parse_list_to_df(data)


edit_compensation_column(df)
edit_city(df)
add_country(df, "Germany")

os.chdir("C:/Users/steve/web-scraping/misc")
df.to_csv("levels_fyi_germany.csv")
df.to_csv("levels_fyi_germany.csv")
os.chdir("C:/Users/steve/web-scraping/database")


df = pd.read_csv("C:/Users/steve/web-scraping/misc/levels_fyi_germany.csv")
df = df.drop(columns="Unnamed: 0", axis=0)

df = df.rename(
    columns={
        "Company": "company_name",
        "Level": "title",
        "Years of Experience": "years_of_experience",
        "Total Compensation": "total_compensation",
        "Salary": "salary",
        "Germany": "country",
    }
)

df_to_sql(df)

df.head(2)
driver.close()
