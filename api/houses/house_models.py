from typing import List, Optional
from pydantic import BaseModel


class Housing_Listing(BaseModel):
    listing_id: str
    title: Optional[str]=None
    price:Optional[str]=None
    description: Optional[str]=None
    latitude: Optional[str]=None
    longitude: Optional[str]=None
    number_of_rooms: Optional[str]=None
    tags:  Optional[List[str]]=None
    facilities:  Optional[List[str]]=None
    amenities: Optional[List[str]]=None
    
    