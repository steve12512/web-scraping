from fastapi import APIRouter
from .house_models import Housing_Listing
from fastapi import Depends

house_router = APIRouter(
    prefix='/houses',
    tags = ['Houses']
)


@house_router.post('/')
def create_housing_entry(listing: Housing_Listing):
    pass
