from fastapi import FastAPI
from salaries import salaries_functions
app = FastAPI()
from database.crud_functions import write_dataframes_to_db

@app.get('/')
async def read_root():
    netherlands_url = salaries_functions.get_netherlands_url()

    return netherlands_url

@app.get('/items/{item_id}')
async def post_root(item_id = 0,  q=2):
    return f'Item with id: {item_id}'

@app.put('/scraping')
async def put_root(quantity : int):
    #salaries_functions.create_country_file('/mock_directory/mock_file.txt')
    return {'quantity' : quantity}

print('1')