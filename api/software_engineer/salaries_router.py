from typing import List, Optional
from typing_extensions import Literal
from fastapi import APIRouter
from .salaries_models import Software_Engineer_Salaries
from database.software_engineer.crud_functions import *
from json import dumps


salaries_router = APIRouter(prefix="/salaries", tags=["Salaries"])


@salaries_router.get("/", response_model=List[Software_Engineer_Salaries])
def get_salaries(limit: int | None):
    salaries = get_all_salaries(limit)
    return salaries


@salaries_router.get("/{country}", response_model=List[Software_Engineer_Salaries])
def get_country_salaries(
    country: Literal[
        "Sweden",
        "Norway",
        "France",
        "Estonia",
        "United Kingdom",
        "Netherlands",
        "Spain",
        "Austria",
        "London",
        "Poland",
        "Ireland",
        "Germany",
    ],
    limit: int | None = None,
):
    salaries = get_country_salaries(country, limit)
    return salaries


@salaries_router.get("{country}/stats")
def get__min_max_avg_country_salaries_per_level(
    country: Literal[
        "Sweden",
        "Norway",
        "France",
        "Estonia",
        "United Kingdom",
        "Netherlands",
        "Spain",
        "Austria",
        "London",
        "Poland",
        "Ireland",
        "Germany",
    ],
    level: Optional[Literal["Senior", "Mid", "Junior"]] = None,
):
    tuple_result = find_min_max_avg_country_salaries(country, level)
    result = {
        "Minimum Salary": tuple_result[0],
        "Average Salary": tuple_result[1],
        "Maximum Salary": tuple_result[2],
    }
    return result


@salaries_router.get("{country}/offerings")
def get_most_offerings_per_country_salaries_for_level(
    country: Literal[
        "Sweden",
        "Norway",
        "France",
        "Estonia",
        "United Kingdom",
        "Netherlands",
        "Spain",
        "Austria",
        "London",
        "Poland",
        "Ireland",
        "Germany",
    ],
    level: Optional[Literal["Senior", "Mid", "Junior"]] = None,
):
    tuple_result = find_most_offerings_per_country_salaries_for_level(country, level)
    result = [{listing[0]: listing[1]} for listing in tuple_result]
    return result
