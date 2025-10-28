from sqlmodel import Field, SQLModel, Session, create_engine, select


class Software_Engineer(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    guid: str
    specialization: str
    city: str
    companyName: str
    totalCompensation: float
    totalCompensationNumber: float
    totalCompensationDetails: str
    baseSalary: float
    baseSalaryNumber: float
    oldYearForData: float
    otherContext: str
    country: str


class software_engineer_salaries(SQLModel, table=True):
    __tablename__ = "software_engineer_salaries"

    id: int | None = Field(default=None, primary_key=True)
    company_name: str | None = None
    title: str | None = None
    years_of_experience: str | None = None
    city: str | None = None
    total_compensation: str | None = None
    salary: float | None = None
    country: str | None = None


