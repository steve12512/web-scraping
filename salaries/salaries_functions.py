import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pprint
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import demjson3
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
from dotenv import load_dotenv

def get_netherlands_url():
    return 'https://techpays.com/europe/netherlands'

def create_country_file(country:str):
    file = country + '_salaries.txt'
    if not os.path.exists(file):
        with open('netherlands_salaries.txt', 'w', encoding= 'utf-8') as f:
            pass



def write_jobs_to_txt(soup, country):
    
    jobs = []
    parsing_dict = False
    whole_response = soup.prettify()
    
    for line in whole_response.splitlines():
        if 'let COMPENSATION_LIST' in line:
            jobs.append(line)
            parsing_dict = True
        
        if parsing_dict:
            jobs.append(line)
        
        if  '];' in line:
            break
        
    with open(f'responses/{country}_salaries.txt', 'w', encoding= 'utf-8') as f:
        for line in jobs:
            f.write(line)
    print('Wrote jobs dictionary.')


def get_country_or_city(country_url:str ) -> str:
    if 'netherlands' in country_url:
        country = 'netherlands'
    else:
        country = 'berlin'
    return country  
            
def scrape_pages(country_url, max_pages_to_be_parsed = 107):
    driver = webdriver.Chrome()
    driver.get(country_url)
    time.sleep(3)
    count = 0
    
    country = get_country_or_city(country_url)
    
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if count == max_pages_to_be_parsed:
            break
        try:
            write_jobs_to_txt(soup, country)
            next_button = driver.find_element(By.XPATH, '//a[contains(@onclick, "gotoNextPage()")]')
            if next_button:
                driver.execute_script("gotoNextPage()")
                time.sleep(3)
                count += 1
                print(f'Clicked next button for the {count}th time')
        except (NoSuchElementException, ElementClickInterceptedException):
            print("No more pages or cannot click next.")
            break
    driver.close()
    
    
def parse_response_to_csv(country:str):
    
    file = parse_response_to_dataframe(country)
    file.to_csv(f'dataframes/{country}_salaries.txt')
    
def parse_response_to_dataframe(country:str) -> pd.DataFrame:

    columns = ['title', 'guid', 'specialization', 'city', 'companyName', 'totalCompensation', 'totalCompensationNumber', 'totalCompensationDetails', 'baseSalary', 'baseSalaryNumber', 'oldYearForData', 'otherContext']
    df = pd.DataFrame([], columns = columns)
    
    with open(f'responses/{country}_salaries.txt', 'r', encoding = 'utf-8') as f:
        content = f.read()
        start = content.rfind('[')
        end = content.rfind(']') + 1
        javascript_string = content[start:end]
        json_string = demjson3.decode(javascript_string) # since our content is a js object and not valid json, we need to decode it like this, for its keys dont have literals in front of them
        df = pd.DataFrame(json_string, columns= columns)
        return df

    
def get_page_filter_button_types_list():
    arguments = ['locationFilterButton','jobFamilyFilterButton', 'seniorityFilterButton','roleTypeFilterButton','companyFilterButton']
    return arguments

def get_dataframe(country:str) -> pd.DataFrame:
    file_path = f'dataframes/{country}_salaries.csv'
    df = pd.read_csv(file_path)
    df_with_modified_columns = modify_df_column_types(df)
    return df_with_modified_columns


def modify_df_column_types(df):
    if 'Unnamed: 0' in df.columns:
        df = df.drop('Unnamed: 0', axis = 1)    
    float_columns = [
        'totalCompensation',
        'totalCompensationNumber',
        'baseSalary',
        'baseSalaryNumber',
        'oldYearForData'
    ]
    for col in float_columns:
        df[col] = pd.to_numeric(df[col], errors = 'coerce')
    str_cols = ['title', 'guid', 'specialization', 'city', 'companyName', 
            'totalCompensationDetails', 'otherContext']
    for col in str_cols:
        df[col] = df[col].astype(str)
    print('newa')
    return df


def scrape_from_fyi(country:str):
    pass


    # <input aria-invalid="false" id="«r0»" placeholder="Email Address" class= type="text" value="" name="username">

def accept_cookies(driver):
    try:
        # Wait for the cookie banner to appear
        cookie_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Accept All")]'))
        )
        cookie_button.click()
        print("Cookies accepted.")
    except:
        print("No cookie banner appeared or already accepted.")


def random_click(driver):
    driver.execute_script("document.elementFromPoint(10, 10).click();")


def sign_in_levels_fyi(driver):
    driver.get('https://www.levels.fyi/login?screen=signIn&from=navbar_buttons')
    email_input = driver.find_element(By.XPATH, '//input[@placeholder="Email Address"]')
    password_input = driver.find_element(By.CSS_SELECTOR,'input[placeholder="Password"]')

    email = os.getenv('email')
    password = os.getenv('password')
    
    email_input.send_keys(email)
    password_input.send_keys(password)

    sign_in_button = driver.find_element(By.XPATH, '//button[text()="Sign In"]')
    pprint.pprint(sign_in_button)
    accept_cookies(driver)
    sign_in_button.click()
    time.sleep(5)

        
def scrape_pages_for_lyi(driver):
    count = 0
    df = pd.DataFrame(columns=['company', 'level name', 'years of experience', 'total compensation'])
    
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            df = scrape_lyi_page(df, soup)
            go_to_next_lyi_page(driver)
            count +=1
            print(f'Clicked next button for the {count}th time')
            
        except (NoSuchElementException, ElementClickInterceptedException):
            print("No more pages or cannot click next.")
            # write_jobs_to_txt(soup, country)
                
    
def go_to_next_lyi_page(driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//button[normalize-space(text())="2"]'))
    ).click()


def scrape_ly_page(df, soup):
    pass    