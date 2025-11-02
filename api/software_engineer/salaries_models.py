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
