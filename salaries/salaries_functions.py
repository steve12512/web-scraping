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
            
            
            
def scrape_pages(country_url):
    driver = webdriver.Chrome()
    driver.get(country_url)
    time.sleep(3)
    count = 0
    
    if 'netherlands' in country_url:
        country = 'netherlands'
    else:
        country = 'berlin'
    
    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        if count == 107:
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
    
    
def parse_to_csv(country):
    
    columns = ['title', 'guid', 'specialization', 'city', 'companyName', 'totalCompensation', 'totalCompensationNumber', 'totalCompensationDetails', 'baseSalary', 'baseSalaryNumber', 'oldYearForData', 'otherContext']
    df = pd.DataFrame([], columns = columns)
    
    
    with open(f'responses/{country}_salaries.txt', 'r', encoding = 'utf-8') as f:
        content = f.read()
        start = content.rfind('[')
        end = content.rfind(']') + 1
        javascript_string = content[start:end]
        json_string = demjson3.decode(javascript_string) # since our content is a js object and not valid json, we need to decode it like this, for its keys dont have literals in front of them
        #json = json.loads(json_string) # would have worked with valid json key-value pairs
        file = pd.DataFrame(json_string, columns= columns)
        file.to_csv(f'dataframes/{country}_salaries.txt')