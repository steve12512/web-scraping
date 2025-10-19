from typing import List
from pymongo import MongoClient
from houses.logger import get_logger

logger = get_logger()
details = 'mongodb://localhost:27017' 
client = MongoClient(details)

db = client['Local']

def get_db():
    yield db
    
def insert_listing(db, listing:dict):
    collection = db['houses']
    if collection.find_one({"listing_id": listing["listing_id"]}):
        return f'Listing with id {listing["listing_id"]} already exists in the collection.'
    collection.insert_one(listing)
    return f'Inserted listing with id; {listing["listing_id"]} in the collection.'
    
    
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