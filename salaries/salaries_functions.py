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


def accept_cookies(driver):
    try:
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
    elements = list()
    
    is_at_second_page = True
    
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            
            elements_of_this_individual_page = scrape_lyi_page(soup)
            
            for listing in elements_of_this_individual_page:
                print(listing)
                
            elements.extend(elements_of_this_individual_page)
            
            go_to_next_lyi_page(driver, is_at_second_page)
            
            count +=1
            if count == 100:
                break
            is_at_second_page = False
            
        except (NoSuchElementException, ElementClickInterceptedException):
            print("No more pages or cannot click next.")
    
    return elements
    
def go_to_next_lyi_page(driver, is_at_second_page=None):
    if is_at_second_page:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[normalize-space(text())="2"]'))
        ).click()
    else:
        try:
            next_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[3]/div[2]/div[2]/table/tfoot/tr/td/div/div[2]/div/button[7]')
            next_button.click()
        except NoSuchElementException:
            print('skipped 1 page')










def scrape_lyi_page(soup):
    
    rows = soup.find_all('tr', class_='salary-row_collapsedSalaryRow__o3k4j')
    elements_of_this_individual_page = []
    
    for row in rows:
        company_tag = row.find(class_='salary-row_companyName__8K8vS')  
        company = company_tag.get_text(strip=True) if company_tag else 'N/A'

        levels_tag = row.find(class_='salary-row_levelName__VZtUC')
        
        levels = levels_tag.get_text(strip=True) if levels_tag else 'N/A'
        
        yoe_tag = row.find('p', class_='css-4g68tt')
        yoe = yoe_tag.get_text(strip=True) if yoe_tag else 'N/A'
        
        total_compensation_tags = row.find_all('span', class_='css-b4wlzm')
        total_compensation = total_compensation_tags[2].get_text(strip=True) if total_compensation_tags else 'N/A'    
        
        city_tag = row.find(class_ = 'css-xlmjpr')
        city = city_tag.get_text(strip=True) if city_tag else 'N/A'    
    
        elements_of_this_individual_page.append([company, levels, yoe, city, total_compensation])
        
    return elements_of_this_individual_page




def parse_list_to_df(elements:list):
    rows = []
    try:
        for row in elements:
            if len(row) >= 4:
                rows.append({
                    'Company' : row[0],
                    'Level' : row[1],
                    'Years of Experience' : row[2],
                    'City' : row[3],
                    'Total Compensation' : row[4]
                })
    except Exception as e:
        print(e.with_traceback)
    df = pd.DataFrame(rows)
    return df




def convert_cols_to_float(df):
    float_cols = [
        'totalCompensation',
        'totalCompensationNumber',
        'baseSalary',
        'baseSalaryNumber',
        'oldYearForData'
    ]
    
    for col in float_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')  # convert, set invalid parsing to NaN
    print(df.dtypes)
    return df


def edit_compensation_column(df):
    
    if 'Total Compensation' in df.columns:
        df['Salary'] = df['Total Compensation'].apply(lambda x: x.split('|')[0])
        df['Salary'] = (df['Salary']
                    .str.extract(r"([\d.,]+)")    
                    .fillna("")                    
                    [0]
                    .str.replace(",", ".", regex=False) 
                )
        
def edit_city(df):
    df['City'] = df['City'].apply(lambda x: x.split('|')[0])
        
def add_country(df, country:str):
    df['country'] = country