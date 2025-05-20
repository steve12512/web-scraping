from sqlmodel import Field, SQLModel, Session, create_engine, select

class software_engineer(SQLModel, table = True):
    id : int | None = Field(default=None, primary_key= True)
    title : str
    city : str
    companyName : str
    title : str
    guid :str 
    specialization : str
    city : str
    totalCompensation : float
    totalCompensationNumber : float
    totalCompensationDetails : str
    baseSalary : float
    baseSalaryNumber : float
    oldYearForData : float
    otherContext : str 



engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
with Session(engine) as session:
    statement = select(software_engineer).where(software_engineer.id == 0)
    result = session.exec(statement).first()
    print(result)