from sqlmodel import Field, SQLModel, Session, create_engine, select

class Software_Engineer(SQLModel, table = True):
    id : int | None = Field(default=None, primary_key= True)
    title : str
    guid :str 
    specialization : str
    city : str
    companyName : str
    totalCompensation : float
    totalCompensationNumber : float
    totalCompensationDetails : str
    baseSalary : float
    baseSalaryNumber : float
    oldYearForData : float
    otherContext : str 



# engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
# with Session(engine) as session:
#     statement = select(Software_Engineer).where(Software_Engineer.id == 0)
#     result = session.exec(statement).first()
#     print(result)