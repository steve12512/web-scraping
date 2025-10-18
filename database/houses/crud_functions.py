from pymongo import MongoClient

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
    