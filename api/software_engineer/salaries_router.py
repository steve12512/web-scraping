from typing import List, Optional
from fastapi import APIRouter
from .salaries_models import Software_Engineer_Salaries
from database.software_engineer.crud_functions import *



salaries_router = APIRouter(prefix="/salaries", tags=["Salaries"])

@salaries_router.get('/', response_model=List[Software_Engineer_Salaries])
def get_salaries(limit:int | None):
    salaries = get_all_salaries(limit)
    return salaries


@salaries_router.get('/{country}', response_model=List[Software_Engineer_Salaries])
def get_country_salaries(country:str, limit:int | None = None):
    salaries = find_country_salaries(country,limit)
    return salaries