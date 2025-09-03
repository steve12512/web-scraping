from sqlmodel import Field, SQLModel, Session, create_engine, select
import pandas as pd
from typing import Type
from models import Software_Engineer


def write_dataframes_to_db(df : pd.DataFrame, model : Type[SQLModel]):
    '''
    '''
    # the commented lines below will have to be deleted
        
    # float_cols = [
    #     'totalCompensation',
    #     'totalCompensationNumber',
    #     'baseSalary',
    #     'baseSalaryNumber',
    #     'oldYearForData'
    # ]
    
    # for col in float_cols:
    #     if col in df.columns:
    #         df[col] = pd.to_numeric(df[col], errors='coerce')  # convert, set invalid parsing to NaN
    # print(df.dtypes)
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    SQLModel.metadata.create_all(engine)
    
    entries = []
    for i, row in df.iterrows():
        model_entry = model(**row.to_dict())
        entries.append(model_entry)
        
    with Session(engine) as session:
        session.add_all(entries)
        session.commit()
        


def find_entry(id:str):
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    with Session(engine) as session:
        statement = select(Software_Engineer).where(Software_Engineer.id == 0)
        result = session.exec(statement).first()
        print(result)
