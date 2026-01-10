from typing import List, Optional
from pydantic import BaseModel


class Software_Engineer_Salaries(BaseModel):
    company_name: Optional[str]
    title: Optional[str]
    years_of_experience: Optional[str]
    city: Optional[str]
    total_compensation: Optional[str]
    salary: Optional[float]
    country: Optional[str]


class Locations(BaseModel):
    country: str
    city: str
    url: str
    max_number_of_listings_to_be_scraped: int
    save_to_db : bool

class Locations_to_scrape(BaseModel):
    locations: List[Locations]
