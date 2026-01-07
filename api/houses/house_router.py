from typing import List, Optional
from fastapi import APIRouter
from .house_models import Housing_Listing
from fastapi import Depends, Query
from database.houses.crud_functions import (
    get_db,
    get_listings,
    get_country_listings,
    get_city_listings,
)
from services.houses.houses_scraping_orchestrator import House_Scraping_Orchestrator
from api.enums.country import Country
from api.enums.city import City

house_router = APIRouter(prefix="/houses", tags=["Houses"])


@house_router.post("/")
def scrape_houses_and_save_them_to_db(
    listing: Housing_Listing,
    max_number_of_listings_to_be_scraped: int = Query(1000, ge=1, le=1000),
    db=Depends(get_db),
):
    """
    Note that the least amount of listings that can be scraped is 16, because the evaluation
    of the condition takes place after a page has been scraped(a page contains 2 containers,
    with each container containing 8 listings)
    """
    places_to_be_scraped = {
        "Stockholm": [
            "Stockholm",
            "Sweden",
            "https://housinganywhere.com/s/Stockholm--Sweden",
            "se",
            max_number_of_listings_to_be_scraped,
        ],
        "Barcelona": [
            "Barcelona",
            "Spain",
            "https://housinganywhere.com/s/Barcelona--Spain",
            "es",
            max_number_of_listings_to_be_scraped,
        ],
        "London": [
            "London",
            "UK",
            "https://housinganywhere.com/s/London--United-Kingdom",
            "gb",
            max_number_of_listings_to_be_scraped,
        ],
        "Amsterdam": [
            "Amsterdam",
            "Netherlands",
            "https://housinganywhere.com/s/Amsterdam--Netherlands",
            "nl",
            max_number_of_listings_to_be_scraped,
        ],
    }
    houses_orchestrator = House_Scraping_Orchestrator(places_to_be_scraped)
    houses_orchestrator.run()


@house_router.get("/", response_model=List[dict])
def get_house_listings(db=Depends(get_db), max_listings: Optional[int] = None):
    listings: List[dict] = get_listings(db, max_listings)
    return listings


@house_router.get("/{country}", response_model=List[dict])
def get_country_house_listings(
    country: Country , db=Depends(get_db), max_listings: Optional[int] = None
):
    country_listings = get_country_listings(db, country, max_listings)
    return country_listings


@house_router.get("/{city}", response_model=List[dict])
def get_city_house_listings(
    city: str, db=Depends(get_db), max_listings: Optional[int] = None
):
    city_listings = get_city_listings(db, city)
    return city_listings
