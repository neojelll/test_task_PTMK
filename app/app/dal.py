from sqlalchemy import create_engine, Column, Integer, String, Date, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .logger import configure_logger
from datetime import datetime
from loguru import logger
import functools
import time


configure_logger()


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    birth_date = Column(Date, nullable=False)
    gender = Column(String, nullable=False)

    def age(self):
        return (datetime.now().date() - self.birth_date).days // 365
    

def log_execution_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.debug(f"{func.__name__} - Execution time: {execution_time} seconds")
        return result
    return wrapper


class EmployeeDAL:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.session = sessionmaker(bind=self.engine)()

    def create_table(self):
        Base.metadata.create_all(self.engine)

    def add_employee(self, full_name, birth_date, gender):
        employee = Employee(full_name=full_name, birth_date=birth_date, gender=gender)
        self.session.add(employee)
        self.session.commit()

    def list_employees(self):
        employees = self.session.query(Employee).order_by(Employee.full_name).all()
        for emp in employees:
            logger.info(f"{emp.full_name}, {emp.birth_date}, {emp.gender}, {emp.age()}")
        return employees

    @log_execution_time
    def query_male_f_employees(self):
        employees = (
            self.session.query(Employee)
            .filter(Employee.gender == "Male", Employee.full_name.like("F%"))
            .all()
        )
        for emp in employees:
            logger.info(f"{emp.full_name}, {emp.birth_date}, {emp.gender}, {emp.age()}")
        return employees

    def optimize_and_query_male_f_employees(self):
        with self.session.begin():
            self.session.execute(
                text("CREATE INDEX IF NOT EXISTS idx_gender ON employees (gender)")
            )
            self.session.execute(
                text(
                    "CREATE INDEX IF NOT EXISTS idx_full_name ON employees(full_name);"
                )
            )
            self.query_male_f_employees()
            logger.debug("Optimization completed.")
