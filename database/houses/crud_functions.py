from typing import List
from pymongo import MongoClient
from houses.logger import get_logger

logger = get_logger()
details = 'mongodb://localhost:27017' 
client = MongoClient(details)


def get_db():
    db = client['HousesDB']
    yield db
    
def insert_listing(db, listing:dict):
    logger.info(f'Type of listing is; {listing.__class__}')
    try:
        collection = db['houses']
        logger.info('Got collection')
        # try:
        #     if collection.find_one({"listing_id": listing["listing_id"]}):
        #         logger.error(f'Listing with id {listing["listing_id"]} already exists in the collection.')
        # except:
        #     logger.error(f'An error occured while trying to find whether or not a listing with id {listing['listing_id']} already exists.')
        collection.insert_one(listing)
        logger.info(f'Inserted listing with id; {listing["listing_id"]} in the collection.')
    except Exception as e:
        logger.error(f'Encountered Exception while trying to insert a listing into the db. {e}')
    
def insert_listings(db, batch:List[dict]):
    try:
        if len(batch) > 0:
            collection = db['houses']
            logger.info('Inserting listings')
            collection.insert_many(batch)
        else:
            logger.error('Batch is empty, cant insert any listings')
    except Exception as e:
        logger.error(f'An exception occured while trying to insert the listings in the db. {e}')