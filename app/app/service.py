from .dal import EmployeeDAL
from datetime import datetime, timedelta
import random
import os


DB_URL = os.environ["DB_URL"]


class EmployeeService():
	def __init__(self):
		self.dal = EmployeeDAL(DB_URL)

	def create_table(self):
		self.dal.create_table()

	def add_employee(self, full_name, birth_date, gender):
		self.dal.add_employee(full_name, birth_date, gender)

	def list_employees(self):
		self.dal.list_employees()

	def generate_random_employees(self, count):
		first_names = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "David", "Anna", "Chris", "Laura"]
		last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]
		genders = ["Male", "Female"]
		for _ in range(count):
			full_name = f"{random.choice(last_names)} {random.choice(first_names)} {random.choice(['A', 'B', 'C'])}"
			birth_date = datetime.now() - timedelta(days=random.randint(18*365, 60*365))
			gender = random.choice(genders)
			self.dal.add_employee(full_name, birth_date.date(), gender)

	def generate_specific_employees(self, count):
		for _ in range(count):
			full_name = f"F{random.choice(['red', 'rank', 'isher'])} {random.choice(['John', 'Jane'])} {random.choice(['A', 'B', 'C'])}"
			birth_date = datetime.now() - timedelta(days=random.randint(18*365, 60*365))
			self.dal.add_employee(full_name, birth_date.date(), "Male")

	def query_male_f_employees(self):
		self.dal.query_male_f_employees()

	def optimize_and_query_male_f_employees(self):
		self.optimize_and_query_male_f_employees()
