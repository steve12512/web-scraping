from sqlmodel import Field, SQLModel, Session, create_engine, select
import pandas as pd
from typing import Type
from models import Software_Engineer, Software_Engineer_Levels_Fyi


from sqlmodel import Field, SQLModel, Session, create_engine, select
from sqlalchemy import text

def write_dataframes_to_db(df : pd.DataFrame, model : Type[SQLModel]):
    '''
    '''
    # the floats to numeric function was called here, before i put it outside of the function
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    SQLModel.metadata.create_all(engine)
    
    entries = []
    for i, row in df.iterrows():
        model_entry = model(**row.to_dict())
        entries.append(model_entry)
    print(entries[0].__dict__)

    with Session(engine) as session:
        session.add_all(entries)
        session.commit()
        


def get_engine():
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    return engine



def df_to_sql(df, table):
    engine = get_engine()
    df.to_sql(table, con=engine, if_exists="append", index=False)



def find_entry(id:str):
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
    with Session(engine) as session:
        statement = select(Software_Engineer).where(Software_Engineer.id == 0)
        result = session.exec(statement).first()
        print(result)




def execute_query(df: pd.DataFrame, query :str, engine) -> list | None:
    
    with Session(engine) as session:
        result = session.exec(text(query))
        rows = result.all()
        
    for row in rows: 
        print(row)
    return rows
