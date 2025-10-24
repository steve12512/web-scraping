from datetime import datetime
from typing import List
from bson import ObjectId
from pymongo import MongoClient
from services.houses.logger import get_logger

logger = get_logger()
details = "mongodb://localhost:27017"
client = MongoClient(details)


def get_db():
    db = client["HousesDB"]
    yield db


def insert_listing(db, listing: dict):
    logger.info(f"Type of listing is; {listing.__class__}")
    try:
        collection = db["houses"]
        logger.info("Got collection")
        if collection.find_one({"listing_id": listing["listing_id"]}):
            logger.error(
                f'Listing with id {listing["listing_id"]} already exists in the collection.'
            )
        else:
            collection.insert_one(listing)
            logger.info(
                f'Inserted listing with id; {listing["listing_id"]} in the collection.'
            )
    except Exception as e:
        logger.error(
            f"Encountered Exception while trying to insert a listing into the db. {e}"
        )


def insert_listings(db, batch: List[dict]):
    logger.info("Inside the insert listings function")
    try:
        if len(batch) > 0:
            collection = db["houses"]
            logger.info("Inserting listings")
            collection.insert_many(batch)
        else:
            logger.error("Batch is empty, cant insert any listings")
    except Exception as e:
        logger.error(
            f"An exception occured while trying to insert the listings in the db. {e}"
        )


def serialize_batch(batch: List[dict]) -> List[dict]:
    logger.info("Inside the serialize batch function")
    return [
        {
            k: str(v) if isinstance(v, (ObjectId, datetime)) else v
            for k, v in listing.items()
        }
        for listing in batch
    ]


def get_listings(db, max_listings=None):
    logger.info("Inside the get_listings function")
    try:
        collection = db["houses"]
        if max_listings is None:
            listing_cursor = collection.find()
        else:
            listing_cursor = collection.find().limit(max_listings)
        listings = list(listing_cursor)
        serialized_listings = serialize_batch(listings)
        return serialized_listings
    except Exception as e:
        logger.error(f"An exception occured while trying to fetch listings\n.{e}")


def get_country_listings(db, country: str, max_listings=None):
    logger.info("Inside the get country listings function, for country {country}")
    try:
        collection = db["houses"]
        logger.info("Got collection")
        if max_listings is None:
            country_listings_cursor = collection.find({"country": country})
        else:
            country_listings_cursor = collection.find({"country": country}).limit(
                max_listings
            )
        logger.info(f"Got country listings for country {country}")
        country_listings = list(country_listings_cursor)
        serialized_listings = serialize_batch(country_listings)
        return serialized_listings
    except Exception as e:
        logger.error(
            f"An exception occured while trying to get country listings \n {e}"
        )


def get_city_listings(db, city: str, max_listings=None):
    logger.info("Inside the get country listings function, for country {country}")
    try:
        collection = db["houses"]
        logger.info("Got collection")
        if max_listings is None:
            country_listings_cursor = collection.find({"country": city})
        else:
            country_listings_cursor = collection.find({"country": city}).limit(
                max_listings
            )
        logger.info(f"Got country listings for country {city}")
        country_listings = list(country_listings_cursor)
        serialized_listings = serialize_batch(country_listings)
        return serialized_listings
    except Exception as e:
        logger.error(f"An exception occured while trying to get city listings \n {e}")
