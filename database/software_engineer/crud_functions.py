from sqlmodel import Field, SQLModel, Session, create_engine, select
import pandas as pd
from typing import Type
from database.software_engineer.models import (
    Software_Engineer,
    software_engineer_salaries,
)
from sqlmodel import Field, SQLModel, Session, create_engine, select
from sqlalchemy import text
from services.salaries.logger import get_logger
from database.software_engineer.models import software_engineer_salaries
from typing import List
import os

logger = get_logger()
DATABASE_URL = os.getenv("DATABASE_URL")

logger.info("Trying to create the engine")
if DATABASE_URL is not None:
    engine = create_engine(DATABASE_URL, echo=True)
    logger.info("Created the database engine")
    SQLModel.metadata.create_all(engine)
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


def convert_list_to_sql_model_and_return_a_list_of_models(df, country: str, city: str):
    logger.info("Inside the convert list to sql model function")
    try:
        sql_models = [
            software_engineer_salaries(
                company_name=row[0],
                title=row[1],
                years_of_experience=row[2],
                city=city,
                salary=float(row[6]),
                country=country,
            )
            for row in df.iter_rows()
        ]
        return sql_models
    except Exception as e:
        logger.error(
            f"An exception occured whilst trying to convert listing into an sql model object. \n {e}"
        )


def add_listings_to_db(models: List[software_engineer_salaries]):
    logger.info(
        "Inside the add listings to db function for the database.software engineers crud functions directory"
    )
    try:
        session = next(get_db())
        logger.info("Successfully got the session object")
        session.add_all(models)
        session.commit()
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
