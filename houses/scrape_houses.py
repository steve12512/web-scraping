from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECfrom
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import json
import zipfile
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from json import dump
from database.houses.crud_functions import get_db, insert_listing
from houses.logger import get_logger
from pathlib import Path

class House_Scraper:

    logger = get_logger()

    def __init__(
        self,
        country="Germany",
        city="Berlin",
        url="https://housinganywhere.com/",
        word_to_split_listing_id_on_the_url="de",
    ):

        self.country = country
        self.city = city
        self.url = url
        self.driver = webdriver.Chrome()
        self.word_to_split_listing_id_on_the_url = word_to_split_listing_id_on_the_url

    def random_click(self, driver):
        driver.execute_script("document.elementFromPoint(10, 10).click();")

    def search_for_place(self, driver, city, url="https://housinganywhere.com/"):
        self.logger.info("Trying to click on url")
        driver.get(url)
        self.logger.info(f"Clicked on url {url}")

    # the lines below were used when we were trying to search for a place, by going to the first screen, and searching for a city parameter that was procided to this function
    # however, that produced random errors, so in the new approach we are directly entering the first page after having searched for the city we want to scrape data for.

    # place_to_search = driver.find_element(By.CSS_SELECTOR, ".css-19wcaby-input-input")
    # change this line to this;
    #     place_to_search = WebDriverWait(driver, 10).until(
    # EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder*='Search']"))
    #     )
    #     place_to_search.send_keys(city)
    #     search_button = driver.find_element(By.CSS_SELECTOR, "button[data-test-locator='Search and book']")
    #     search_button.click()
    #     self.logger.info('Clicked on search button')
    #     self.random_click(driver)
    #     self.logger.info('Clicked on random place')
    #     self.logger.info('Clicked on search button again')
    #     search_button.click()

    def scroll_page(self, driver):
        new_height = driver.execute_script("return document.body.scrollHeight")

    def press_escape(self, driver):
        driver.switch_to.active_element.send_keys(Keys.ESCAPE)

    def accept_cookies(self, driver):
        time.sleep(2)
        cookies_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookies_button.click()

    def create_directory_for_photos(self):
        self.logger.info(
            f"Trying to create the directory; house_photos/{self.country}_{self.city}_house_photos"
        )
        try:
            if not os.path.exists(
                f"houses/house_photos/{self.country}_{self.city}_house_photos"
            ):
                os.makedirs(
                    f"houses/house_photos/{self.country}_{self.city}_house_photos"
                )
                self.logger.info(
                    f"Successfully created the directory; houses/house_photos/{self.country}_{self.city}_house_photos"
                )
        except Exception as e:
            self.logger.error(
                f"Failed to create directory; houses/house_photos/{self.country}_{self.city}_house_photos"
            )
            self.logger.error(f"Error is {e}")

    def get_geo_data(self, driver):
        try:
            self.logger.info("Inside the get geo data function")
            latitude, longitude, number_of_rooms = None, None, None
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, "html.parser")
            script_elements = soup.find_all("script", type="application/ld+json")
            for script in script_elements:
                if script.string:
                    data = json.loads(script.string)

                    if data.get("@type") != "Accommodation":
                        continue
                    geo_data = data.get("geo")
                    self.logger.info(f"Got geo data; {geo_data}")
                    latitude = geo_data.get("latitude")
                    self.logger.info(f"Got latitude {latitude}")
                    longitude = geo_data.get("longitude")
                    self.logger.info(f"Got longitude")
                    number_of_rooms = data.get("numberOfRooms")
                    self.logger.info(f"Got number of rooms {number_of_rooms}")
        except:
            self.logger.error("Inside the geo_data function, an Exception has occured")
            return None, None, None

        return latitude, longitude, number_of_rooms

    def get_container(self, driver):
        page_container = driver.find_element(By.CLASS_NAME, "css-wp5dsn-container")
        return page_container

    def get_container_listings(self, container):
        rows = container.find_elements(By.CLASS_NAME, "css-1efwqj7-cardLink")
        return rows

    def scroll_down_a_tiny_bit(self, driver):
        self.logger.info("Inside the scroll down a tiny bit function1")
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(2)

    def scroll_down_and_wait_2_secs(self, driver):
        self.logger.info("In the scroll down and wait 2 secs function")
        driver.execute_script("window.scrollBy(0, 2000);")
        time.sleep(2)

    def get_facilities(self, driver):
        self.logger.info("Inside the get facilities function")
        try:
            facilities = []
            container = driver.find_element(By.CLASS_NAME, "css-1v5feww-container")
            facilities_list = container.find_element(By.CLASS_NAME, "css-scctyu-list")
            list_items = facilities_list.find_elements(By.TAG_NAME, "li")
            for item in list_items:
                facilities.append(item.text)
                self.logger.info(f"Appended facilities item {item.text}")
            return facilities
        except:
            self.logger.error("Did not manage to get listing amenities")
            return []

    def show_more(self, driver):
        self.logger.info("Inside the show more function")
        show_more_button = driver.find_element(
            By.CLASS_NAME, "css-67atf2-button-showMoreButton"
        )
        show_more_button.click()
        self.logger.info("Clicked the show more button")

    def get_amenities(self, driver):
        self.logger.info("Inside the get amenities function")
        amenities = []
        try:
            self.scroll_down_a_tiny_bit(driver)
            self.show_more(driver)
            sub_wrapper = driver.find_elements(By.CLASS_NAME, "css-scctyu-list")
            wrapper = sub_wrapper[-1]
            items = wrapper.find_elements(By.TAG_NAME, "li")
            for item in items:
                amenities.append(item.text)

        except Exception:
            self.logger.error("An error occured whilst trying to get amenities ")
        finally:
            self.logger.info("Trying to close the amenities pupup")
            self.press_escape(driver)
            self.logger.info("Closed the amenities popup")
            return amenities

    def get_listing_tags(self, driver):
        try:
            tags_container = driver.find_element(
                By.CLASS_NAME, "css-q6fy6c-highlightContainer"
            )
            if tags_container:
                container_elements = tags_container.find_elements(
                    By.CLASS_NAME, "css-1e5azn1-highlightItem"
                )
                tags = []
                for tag_element in container_elements:
                    tag = tag_element.text
                    tags.append(tag)
                return tags
        except:
            return [None]

    def get_images(self, driver):
        self.logger.info("Inside the get_images function")
        more_photos_button = driver.find_element(
            By.CLASS_NAME, "css-13emeri-tile-tileButton"
        )
        more_photos_button.click()
        images = driver.find_elements(By.TAG_NAME, "img")
        return images

    def scrape_listing_photos_and_save_them_as_files_in_file_explorer(
        self, driver, listing_id: str
    ):
        self.logger.info(
            "Inside the scrape_listing_photos_and_save_them_as_files_in_file_explorer function "
        )
        self.logger.info(
            f"Trying to create the houses/house_photos/{self.country}_{self.city}_house_photos directory"
        )
        # folder = os.path.join(
        #     f"houses/house_photos/{self.country}_{self.city}_house_photos", listing_id
        # )
        folder = Path("houses") / "house_photos" / f"{self.country}_{self.city}" / f"{listing_id}_house_photos"

        os.makedirs(folder, exist_ok=True)
        images = self.get_images(driver)
        self.logger.info("Got more images")
        unique_images = set(images)
        #zip_file_path = os.path.join(folder, "photos.zip")
        zip_file_path = folder / "photos.zip"
        self.logger.info(f"Created zip file path {zip_file_path}")
        with zipfile.ZipFile(
            zip_file_path, "w", compression=zipfile.ZIP_DEFLATED
        ) as f1:
            self.logger.info(f"Into the zip path {zip_file_path}")
            for i, image in enumerate(unique_images):
                self.logger.info(
                    f"Enumerating the images of listing with id; {listing_id}"
                )
                size = image.size
                height = size["height"]
                if height >= 45:
                    image_url = (
                        image.get_attribute("src")
                        or image.get_attribute("data-src")
                        or image.get_attribute("data-lazy")
                        or image.get_attribute("data-original")
                    )
                    if image_url.startswith("http"):
                        response = requests.get(image_url)
                        image_to_be_written = response.content
                        image_bytes = len(image_to_be_written)
                        if image_bytes > 100 * 1000:
                            image_name = listing_id + "_" + str(i) + ".jpg"
                            self.logger.info(
                                f"Inside listing {listing_id}, trying to write image {image_name}"
                            )
                            f1.writestr(image_name, image_to_be_written)
                            self.logger.info(
                                f"Successfully wrote image, with image name {image_name}"
                            )
                    else:
                        self.logger.error(f"image {i} doesnt start with http")
                        self.logger.error(image_url)
                else:
                    self.logger.info("Image height is lesss than 45")
            if zip_file_path:
                return zip_file_path

    def create_meta_data_object(
        self,
        listing_id,
        title,
        price,
        description,
        tags,
        latitude,
        longitude,
        number_of_rooms,
        facilities,
        amenities,
        photos_folder_path
    ):
        self.logger.info("Inside the create json object function")
        meta_data = {
            "listing_id": listing_id,
            "title": title if title is not None else "N/A",
            "price": price if price is not None else "N/A",
            "description": description if description is not None else "N/A",
            "latitude": latitude if latitude is not None else "N/A",
            "longitude": longitude if longitude is not None else "N/A",
            "number_of_rooms": (
                number_of_rooms if number_of_rooms is not None else "N/A"
            ),
            "tags": list(tags) if len(tags) > 0 else None,
            "facilities": list(facilities) if len(facilities) > 0 else None,
            "amenities": list(amenities) if len(amenities) > 0 else None,
            "photos_folder_path" : photos_folder_path if photos_folder_path is not None else 'N/A'
        }
        return meta_data

    def create_metadata_file_in_the_listings_folder(self, listing_id, meta_data):
        try:
            if not isinstance(listing_id, str):
                self.logger.error(f"Listing with id; {listing_id} is not of type; str")
                raise ValueError
            folder = os.path.join(
                f"houses/house_photos/{self.country}_{self.city}_house_photos",
                listing_id,
            )
            os.makedirs(folder, exist_ok=True)
            self.logger.info(
                f"Created folder or folder already exists for listing with id; {listing_id}"
            )
            file = os.path.join(folder, ".metadata")
            with open(file, "w", encoding="utf-8") as f1:
                json_meta_data = json.dumps(meta_data, ensure_ascii=False, indent=4)
                f1.write(json_meta_data)
                self.logger.info(
                    f"Wrote meta_data file for listing with id; {listing_id}"
                )
        except Exception:
            self.logger.error(
                f"Encountered error during the writing of the Meta Data file for listing with id; {listing_id}"
            )
            self.driver.close()

    def go_up_a_bit(self, driver):
        self.logger.info(
            "******************* In the go up a bit function ******************"
        )
        driver.execute_script("window.scrollBy(0, -2000);")

    def get_listing_text_attributes(self, driver):
        wait = WebDriverWait(driver, 2)
        try:
            title = wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "css-1ql5bbl"))
            ).text
        except:
            title = None
        try:
            price_container = driver.find_element(
                By.CLASS_NAME, "css-iu8lzi-container-containerAlignBaseLine"
            )
            price = price_container.text.split("\n")[0]
        except:
            price = None
        try:
            description = wait.until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, "css-jtt5vl-breakWord-description")
                )
            ).text
        except:
            description = None

        return (
            title,
            price,
            description,
        )

    def get_listing_id(self, driver, word_to_split_listing_id_on_the_url):
        current_url = driver.current_url
        if "/ut" in current_url:
            listing_id = current_url.split("/ut")[1].split(
                word_to_split_listing_id_on_the_url
            )[0]
        else:
            listing_id = current_url.split("-")[-1]
        if "/" in listing_id:
            listing_id = listing_id.split("/")[0]
        return listing_id

    def scroll_up_a_bit(self, driver):
        driver.execute_script("window.scrollBy(0, -1000);")
        time.sleep(2)
        self.logger.info("Scrolled up a bit")

    def scrape_listing(
        self, listing, driver, original_window, word_to_split_listing_id_on_the_url
    ):
        encountered_error = False
        try:
            listing.click()
            self.logger.info("Successfully clicked on listing")
        except Exception:
            self.logger.error("Didn t manage to sclick on listing.")
        try:
            driver.switch_to.window(driver.window_handles[-1])
            listing_id = self.get_listing_id(
                driver, word_to_split_listing_id_on_the_url
            )
            self.logger.info(f"Acquired listing id {listing_id}")

            if listing_id.isdigit():

                title, price, description = self.get_listing_text_attributes(driver)
                self.logger.info(
                    f"Title : {title}, price : {price}, description : {description}"
                )

                tags = self.get_listing_tags(driver)
                self.logger.info(f"Tags : {tags}")

                facilities = self.get_facilities(driver)
                self.logger.info(f"Got facilities for listing with id {listing_id}")

                amenities = self.get_amenities(driver)
                self.logger.info(f"Got amenities for listing with id {listing_id}")

                self.logger.info("Trying to scroll up a bit")
                self.scroll_up_a_bit(driver)

                photos_folder_path = (
                    self.scrape_listing_photos_and_save_them_as_files_in_file_explorer(
                        driver, listing_id
                    )
                )
                self.logger.info(f"Scraped photos and saved them in a local directory")

                latitude, longitude, number_of_rooms = self.get_geo_data(driver)
                self.logger.info(
                    f"Latitude {latitude}, longitude : {longitude}, Number of Rooms : {number_of_rooms}"
                )

                meta_data = self.create_meta_data_object(
                    listing_id,
                    title,
                    price,
                    description,
                    tags,
                    latitude,
                    longitude,
                    number_of_rooms,
                    facilities,
                    amenities,
                    photos_folder_path
                )
                self.logger.info("Exiting from the create meta data object function")

                self.create_metadata_file_in_the_listings_folder(listing_id, meta_data)
                self.logger.info(
                    f"Created metadata file for listing with id ; {listing_id}"
                )

                ########################
                db = next(get_db())
                self.logger.info("Got db")
                insert_listing(db, meta_data)
                self.logger.info(f"Inserted metadata object{meta_data}")
            else:
                self.logger.error(f"{listing_id} is not numeric")

        except Exception:
            self.logger.error("something failed when scraping the data")
            encountered_error = True
        finally:

            if driver.current_window_handle != original_window:
                driver.close()
                driver.switch_to.window(original_window)
                return encountered_error

    def enter_site(self, driver, city, url):
        tries = 0
        while True:
            try:
                # the lines below will have to be deleted.

                # tries += 1
                # if tries == 2:
                #     os.execv(sys.executable, [sys.executable] + sys.argv)
                self.logger.info("Trying to search for place")
                # we can provide the url if we want to start at the first search page of the city we want to scrape, without having first to search for it
                # if we do not provide it(as is the case below) we will search by using the city variable, at the search page.
                self.search_for_place(driver, city, url)
                self.logger.info("Searched for place, trying to accept cookies")
                self.accept_cookies(driver)
                self.logger.info("Accepted cookies")
                break

            except Exception:
                self.logger.error("Exception while trying to search for place")

    def scrape_half_page(self, driver, word_to_split_listing_id_on_the_url):
        try:
            encountered_error = False
            self.logger.info("Trying to get the container element")
            container = driver.find_element(By.CLASS_NAME, "css-wp5dsn-container")

            self.scroll_page(driver)
            self.logger.info("Trying to get the container's listings")
            container_listings = self.get_container_listings(container)

            original_window = driver.current_window_handle
            if len(container_listings) > 0:
                self.logger.info(
                    f"Iterating over the container's listings with len {len(container_listings)}"
                )
                for listing in container_listings:
                    try:
                        self.logger.info(
                            "Trying to scrape a listing from the container"
                        )
                        encountered_error = self.scrape_listing(
                            listing,
                            driver,
                            original_window,
                            word_to_split_listing_id_on_the_url,
                        )
                        if encountered_error:
                            break
                    except ElementClickInterceptedException:
                        self.logger.error(
                            "Failed to scrape a listing from the container"
                        )
            else:
                self.logger.error("This container contained no listings")
        except Exception:
            self.logger.error("Undefined error")
        finally:
            print("containers;", len(container_listings))

    def scrape_page(self, driver, word_to_split_listing_id_on_the_url):
        """
        For each page, scrape its upper half first.
        Then scroll down a bit, to get more container listings, and scrape the other half
        """
        encountered_error = self.scrape_half_page(
            driver, word_to_split_listing_id_on_the_url
        )
        if not encountered_error:
            driver.execute_script("window.scrollBy(0, 2000);")
        else:
            self.go_up_a_bit(driver)
        self.scrape_half_page(driver, word_to_split_listing_id_on_the_url)

    def go_to_next_page(self, driver):
        self.logger.info("Trying to go to the next Page")
        next_button = driver.find_element(
            By.CSS_SELECTOR, "button[aria-label='Go to next page']"
        )
        next_button.click()
        self.logger.info("Clicked on next Page")

    def scrape_pages(self, driver, logger, word_to_split_listing_id_on_the_url):
        logger.info("Started Scraping Pages")
        pages_scraped = 0
        try:
            while True:
                try:
                    logger.info(f"Trying to Scrape the {pages_scraped}th Page")
                    self.scrape_page(driver, word_to_split_listing_id_on_the_url)
                    logger.info(f"Successfuly scraped the {pages_scraped}th Page")

                    pages_scraped += 1

                    logger.info(f"Trying to click on the {pages_scraped}th Page")

                    self.scroll_down_and_wait_2_secs(driver)

                    self.go_to_next_page(driver)

                    if (
                        pages_scraped == 100
                    ):  # we do not need to scrape more than 100 pages
                        logger.info("Scraped 100 pages, Now exiting")
                        break
                except Exception as e:
                    logger.error(
                        f"Encounterd Error during the scraping of the {pages_scraped}th Page",
                        exc_info=True,
                    )
                    logger.error("Attempting to go up a bit")
                    self.go_up_a_bit(driver)
        finally:
            driver.close()

    def scrape_pages_and_save_them(self):
        logger = get_logger()
        driver = self.driver
        url = self.url
        word_to_split_listing_id_on_the_url = self.word_to_split_listing_id_on_the_url
        city = self.city

        self.create_directory_for_photos()
        self.enter_site(driver, city, url)
        self.scrape_pages(driver, logger, word_to_split_listing_id_on_the_url)
