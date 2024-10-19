from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String , Date, text
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, timedelta
import random


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
	def __init__(self, db_url):
		self.engine = create_engine(db_url)
		self.session = sessionmaker(bind=self.engine)()

	def create_table(self):
		Base.metadata.create_all(self.engine)

	def add_employee(self, full_name, birth_date, gender):
		employee = Employee(full_name=full_name, birth_date=birth_date, gender=gender)
		employee.save(self.session)

	def list_employees(self):
		employees = self.session.query(Employee).order_by(Employee.full_name).all()
		for emp in employees:
			print(f"{emp.full_name}, {emp.birth_date}, {emp.gender}, {emp.age()}")

	def generate_random_employees(self, full_name, birth_date, gender, count):
		first_names = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "David", "Anna", "Chris", "Laura"]
		last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
		genders = ["Male", "Female"]
		for _ in range(count):
			full_name = f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(['A', 'B', 'C'])}"
			birth_date = datetime.now() - timedelta(days=random.randint(18*365, 60*365))
			gender = random.choice(genders)
			self.add_employee(full_name, birth_date.date(), gender)

	def generate_specific_employees(self, count):
		for _ in range(count):
			full_name = f"F{random.choice(['red', 'rank', 'isher'])} {random.choice(['John', 'Jane'])} {random.choice(['A', 'B', 'C'])}"
			birth_date = datetime.now() - timedelta(days=random.randint(18*365, 60*365))
			self.add_employee(full_name, birth_date.date(), "Male")

	def query_male_f_employees(self):
		employees = self.session.query(Employee).filter(Employee.gender == "Male", Employee.full_name.like("F%")).all()
		for emp in employees:
			print(f"{emp.full_name}, {emp.birth_date}, {emp.gender}, {emp.age()}")

	def optimize_and_query_male_f_employees(self):
		with self.session.begin():
			self.session.execute(text("CREATE INDEX IF NOT EXISTS idx_gender ON employees (gender)"))
			self.session.execute(text("CREATE INDEX IF NOT EXISTS idx_full_name ON employees(full_name);"))
		self.query_male_f_employees()
