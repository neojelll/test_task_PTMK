import random
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


def create_connection():
	engine = create_engine('postgresql://username:password@localhost:5432/your_database')
	return sessionmaker(bind=engine)()


def create_table(session):
	Base.metadata.create_all(session.bind)


def add_employee(session, full_name, birth_date, gender):
	employee = Employee(full_name=full_name, birth_date=birth_date, gender=gender)
	employee.save(session)


def list_employees(session):
	employees = session.query(Employee).order_by(Employee.full_name).all()
	for emp in employees:
		print(f"{emp.full_name}, {emp.birth_date}, {emp.gender}, {emp.age()}")


def generate_random_employees(session, count):
	first_names = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "David", "Anna", "Chris", "Laura"]
	last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
	genders = ["Male", "Female"]
	for _ in range(count):
		full_name = f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(['A', 'B', 'C'])}"
		birth_date = datetime.now() - timedelta(days=random.randint(18*365, 60*365))
		gender = random.choice(genders)
		add_employee(session, full_name, birth_date.date(), gender)


def generate_specific_employees(session, count):
	for _ in range(count):
		full_name = f"F{random.choice(['red', 'rank', 'isher'])} {random.choice(['John', 'Jane'])} {random.choice(['A', 'B', 'C'])}"
		birth_date = datetime.now() - timedelta(days=random.randint(18*365, 60*365))
		add_employee(session, full_name, birth_date.date(), "Male")


def query_male_f_employees(session):
	employees = session.query(Employee).filter(Employee.gender == "Male", Employee.full_name.like("F%")).all()
	for emp in employees:
		print(f"{emp.full_name}, {emp.birth_date}, {emp.gender}, {emp.age()}")


def optimize_and_query_male_f_employees(session):
    with session.begin():
        session.execute("CREATE INDEX IF NOT EXISTS idx_gender ON employees(gender);")
        session.execute("CREATE INDEX IF NOT EXISTS idx_full_name ON employees(full_name);")
    query_male_f_employees(session)
