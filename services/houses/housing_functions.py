import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pprint
import re
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementClickInterceptedException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC

import os


def get_driver():
    driver = webdriver.Chrome()
    return driver


def create_directory_for_photos():
    if not os.path.exists("house_photos"):
        os.mkdir("house_photos")


def random_click(driver):
    driver.execute_script("document.elementFromPoint(10, 10).click();")


def search_for_place(driver, url="https://housinganywhere.com/"):

    driver.get(url)

    place_to_search = driver.find_element(By.CSS_SELECTOR, ".css-19wcaby-input-input")
    place_to_search.send_keys("Berlin")

    search_button = driver.find_element(
        By.CSS_SELECTOR, "button[data-test-locator='Search and book']"
    )
    search_button.click()

    random_click(driver)
    search_button.click()


def accept_cookies(driver):
    cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
    cookies_button.click()


def scroll_page(driver):
    new_height = driver.execute_script("return document.body.scrollHeight")
