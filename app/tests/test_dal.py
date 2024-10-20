import pytest
from datetime import datetime
from app.dal import EmployeeDAL, Employee


@pytest.fixture(scope="module")
def test_db():
    db_url = "sqlite:///:memory:"
    dal = EmployeeDAL(db_url)
    dal.create_table()
    yield dal
    dal.session.close()


def test_add_employee(test_db):
    test_db.add_employee("John Doe", datetime(1990, 1, 1).date(), "Male")
    test_db.add_employee("Fiona Smith", datetime(1985, 5, 15).date(), "Female")

    employees = test_db.list_employees()
    assert len(employees) == 2
    assert employees[0].full_name == "Fiona Smith"
    assert employees[1].full_name == "John Doe"


def test_query_male_f_employees(test_db):
    test_db.add_employee("Frank Castle", datetime(1980, 2, 16).date(), "Male")
    test_db.add_employee("Fiona Smith", datetime(1985, 5, 15).date(), "Female")

    test_db.optimize_and_query_male_f_employees()
    male_f_employees = test_db.query_male_f_employees()
    assert male_f_employees[0].full_name == "Frank Castle"


def test_employee_age(test_db):
    test_db.add_employee("Alice Johnson", datetime(2000, 1, 1).date(), "Female")
    employee = (
        test_db.session.query(Employee).filter_by(full_name="Alice Johnson").first()
    )
    expected_age = (datetime.now().date() - employee.birth_date).days // 365
    assert employee.age() == expected_age
