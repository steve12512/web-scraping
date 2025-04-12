import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pprint
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import os


def write_jobs_to_txt(soup):
    
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
        
    with open('response_content.txt', 'w', encoding= 'utf-8') as f:
        for line in jobs:
            f.write(line)
    print('Wrote jobs dictionary.')
            
            
            
def scrape_pages(country_url):
    driver = webdriver.Chrome()
    driver.get(country_url)
    time.sleep(3)
    count = 0

    while True:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        try:
            write_jobs_to_txt(soup)
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