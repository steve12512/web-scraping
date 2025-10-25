from sqlmodel import Field, SQLModel, Session, create_engine, select
import pandas as pd
from typing import Type
from database.software_engineer.models import (
    Software_Engineer,
    Software_Engineer_Levels_Fyi,
)
from sqlmodel import Field, SQLModel, Session, create_engine, select
from sqlalchemy import text
from services.salaries.logger import get_logger
from database.software_engineer.models import Software_Engineer_Levels_Fyi
from typing import List
import os

logger = get_logger()
DATABASE_URL = os.getenv("DATABASE_URL")

logger.info("Trying to create the engine")
if DATABASE_URL is not None:
    engine = create_engine(DATABASE_URL, echo=True)
else:
    logger.error("Failed to create the engine")


# def write_dataframes_to_db(df: pd.DataFrame, model: Type[SQLModel]):
#     """ """
#     # the floats to numeric function was called here, before i put it outside of the function
#     engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
#     SQLModel.metadata.create_all(engine)

#     entries = []
#     for i, row in df.iterrows():
#         model_entry = model(**row.to_dict())
#         entries.append(model_entry)
#     print(entries[0].__dict__)

#     with Session(engine) as session:
#         session.add_all(entries)
#         session.commit()


def get_db():
    logger.info(
        "Inside the get db function of the database/software_engineer/crud_functions directory"
    )
    with Session(engine) as session:
        yield session


# ['Datadog', 'Senior Software Engineer', '10  yrs', 'London, EN, United Kingdom | 31 minutes ago', '10,3\xa0χιλ. | 6,2\xa0χιλ. | N/A']
def convert_list_to_sql_model_and_return_a_list_of_models(listings: List):
    logger.info("Inside the convert list to sql model function")
    sql_models = []
    for listing in listings:
        try:
            sql_model = Software_Engineer_Levels_Fyi(
                company_name=listing[0],
                title=listing[1],
                years_of_experience=listing[2],
                city=listing[4],
                salary=float(listing[5]),
                country=listing[6],
            )
            sql_models.append(sql_model)
        except Exception as e:
            logger.error(
                f"An exception occured whilst trying to convert listing {listing} into an sql model object. \n {e}"
            )
    return sql_models


def add_listings_to_db(models: List[Software_Engineer_Levels_Fyi]):
    logger.info(
        "Inside the add listings to db function for the database.software engineers crud functions directory"
    )
    try:
        session = next(get_db())
        logger.info("Successfully got the session object")
        session.add_all(models)
        logger.info("Successfully inserted the objects to the db")
    except Exception as e:
        logger.error(
            f"An Exception occured whilst trying to insert the listings to the db {e}"
        )


# def df_to_sql(df, table):
#     engine = get_engine()
#     df.to_sql(table, con=engine, if_exists="append", index=False)


# def find_entry(id: str):
#     engine = create_engine("postgresql://postgres:postgres@localhost:5432/postgres")
#     with Session(engine) as session:
#         statement = select(Software_Engineer).where(Software_Engineer.id == 0)
#         result = session.exec(statement).first()
#         print(result)


# def execute_query(df: pd.DataFrame, query: str, engine) -> list | None:

#     with Session(engine) as session:
#         result = session.exec(text(query))
#         rows = result.all()

#     for row in rows:
#         print(row)
#     return rows
