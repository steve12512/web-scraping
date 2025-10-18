from fastapi import APIRouter
from .house_models import Housing_Listing
from fastapi import Depends
from database.houses.crud_functions import get_db

house_router = APIRouter(
    prefix='/houses',
    tags = ['Houses']
)


@house_router.post('/')
def create_housing_entry(listing: Housing_Listing, db = Depends(get_db)):
    pass



