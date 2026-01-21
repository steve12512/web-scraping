from typing import List, Optional
from pydantic import BaseModel


class Housing_Listing_Request(BaseModel):
    city:str
    country:str 
    url:str
    word_to_split_page:str
    max_number_of_listings_to_be_scraped:int 