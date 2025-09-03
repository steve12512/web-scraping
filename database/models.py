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




class SoftwareEngineerLevelsFyi(SQLModel, table=True):
    __tablename__ = "software_engineer_levels_fyi"

    id: int | None = Field(default=None, primary_key=True)
    company_name: str | None = None
    title: str | None = None
    years_of_experience: str | None = None
    total_compensation: str | None = None












# engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')
# with Session(engine) as session:
#     statement = select(Software_Engineer).where(Software_Engineer.id == 0)
#     result = session.exec(statement).first()
#     print(result)