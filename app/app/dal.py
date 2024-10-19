from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String , Date, func
from sqlalchemy.orm import sessionmaker, declarative_base


Base = declarative_base()


class Employee(Base):
	__tablename__ = "employees"
	id = Column(Integer, primary_key=True)
	full_name = Column(String, nullable=False)
	birth_date = Column(Date, nullable=False)
	gender = Column(String, nullable=False)

	def age(self):
		return (datetime.now().date() - self.birth_date).days // 365
	
	def save(self, session):
		session.add(self)
		session.commit()


class EmployeeDAL():
	def __init__(self, session):
		self.session = session

	def optimize(self):
		with self.session.begin():
			self.session.execute("CREATE INDEX IF NOT EXISTS idx_gender ON employees(gender);")
			self.session.execute("CREATE INDEX IF NOT EXISTS idx_full_name ON employees(full_name);")
