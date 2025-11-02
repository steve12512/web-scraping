import argparse
from pathlib import Path
from dotenv import load_dotenv
from sqlmodel import Field, SQLModel, Session, create_engine, select
import pandas as pd
from typing import Type
from database.software_engineer.models import (
    Software_Engineer,
    software_engineer_salaries,
)
from sqlmodel import Field, SQLModel, Session, create_engine, select
from sqlalchemy import func, text
from services.salaries.logger import get_logger
from database.software_engineer.models import software_engineer_salaries
from typing import List
import os

logger = get_logger()
env_path = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(dotenv_path=env_path)
DATABASE_URL = os.getenv("DATABASE_URL")
logger.info("Trying to create the engine")
try:
    engine = create_engine(DATABASE_URL, echo=True)
    logger.info("Created the database engine")
    # SQLModel.metadata.create_all(engine)
except Exception as e:
    logger.error(f"Failed to create the engine. {e}")


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


def get_all_salaries(limit: int | None = 500):
    logger.info("Inside the get_all_salaries function")
    with Session(engine) as session:
        statement = select(software_engineer_salaries).limit(limit)
        result = session.exec(statement).all()
        logger.info(f"Successfully ran query. The results are; {result}")
        return result


def find_country_salaries(country: str, limit: int | None = 500):
    logger.info("Inside the find country salaries function")
    with Session(engine) as session:
        statement = (
            select(software_engineer_salaries)
            .where(software_engineer_salaries.country == country)
            .limit(limit)
        )
        result = session.exec(statement).all()
        logger.info(f"Successfully ran query. The results are; {result}")
        return result

def find_min_max_avg_country_salaries(country: str):
    logger.info("Inside the find find_min_max_avg_country_salaries function")
    with Session(engine) as session:
        statement = (
            select(
                func.min(software_engineer_salaries.salary),
                func.avg(software_engineer_salaries.salary),
                func.max(software_engineer_salaries.salary),
            )
            .where(software_engineer_salaries.country == country)
            .group_by(software_engineer_salaries.country)
        )
        result = session.exec(statement).first()
        logger.info(f"Successfully ran query. The results are; {result}")


def find_min_max_avg_country_salaries_for_level(country: str, level: str):
    """
    level should be Senior,Junior, Mid
    """
    logger.info("Inside the find find_min_max_avg_country_salaries_for_level function")
    with Session(engine) as session:
        statement = (
            select(
                func.min(software_engineer_salaries.salary).label("Minimum Salary"),
                func.avg(software_engineer_salaries.salary).label("Average Salary"),
                func.max(software_engineer_salaries.salary).label("Maximum Salary"),
            )
            .where(
                (software_engineer_salaries.country == country)
                & (software_engineer_salaries.title.contains(level))
            )
            .group_by(software_engineer_salaries.country)
            .limit(50)
        )
        result = session.exec(statement).all()
        logger.info(f"Successfully ran query. The results are; {result}")


def find_most_offerings_per_country_salaries_for_level(
    country: str, level: str | None = None
):
    """
    level should be Senior,Junior, Mid
    """
    logger.info(
        "Inside the find find_most_offerings_per_country_salaries_for_level function"
    )
    with Session(engine) as session:
        if level == None:
            statement = calculate_positions_without_level(country)
        else:
            statement = calculate_positions_with_level(country, level)
        result = session.exec(statement).all()
        logger.info(f"Successfully ran query. The results are; {result}")


def calculate_positions_without_level(country: str):
    return (
        select(
            func.count(software_engineer_salaries.company_name).label(
                "Company Hirings"
            ),
            software_engineer_salaries.company_name,
        )
        .where((software_engineer_salaries.country == country))
        .group_by(
            software_engineer_salaries.country,
            software_engineer_salaries.company_name,
        )
        .order_by(func.count(software_engineer_salaries.company_name).desc())
        .limit(50)
    )


def calculate_positions_with_level(country: str, level: str):
    return (
        select(
            func.count(software_engineer_salaries.company_name).label(
                "Company Hirings"
            ),
            software_engineer_salaries.company_name,
        )
        .where(
            (software_engineer_salaries.country == country)
            & (software_engineer_salaries.title.contains(level))
        )
        .group_by(
            software_engineer_salaries.country,
            software_engineer_salaries.company_name,
        )
        .order_by("Company Hirings")
        .limit(50)
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("country", help="Country to query salaries for")
    parser.add_argument("level", help="Job level to filter by")
    args = parser.parse_args()
    find_most_offerings_per_country_salaries_for_level(args.country, args.level)
