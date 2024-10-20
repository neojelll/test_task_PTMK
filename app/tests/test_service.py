import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime
from app.service import EmployeeService


@pytest.fixture
def employee_service(mocker):
	with patch.dict('os.environ', {'DB_URL': 'sqlite:///:memory:'}):
		mock_dal = mocker.patch('app.service.EmployeeDAL', autospec=True, return_value=MagicMock())
		service = EmployeeService()
		service.dal = mock_dal.return_value
		return service


def test_create_table(employee_service):
    employee_service.create_table()
    employee_service.dal.create_table.assert_called_once()


def test_add_employee(employee_service):
    full_name = "John Doe A"
    birth_date = datetime(1990, 1, 1).date()
    gender = "Male"
    employee_service.add_employee(full_name, birth_date, gender)
    employee_service.dal.add_employee.assert_called_once_with(full_name, birth_date, gender)


def test_list_employees(employee_service):
    employee_service.list_employees()
    employee_service.dal.list_employees.assert_called_once()


def test_generate_random_employees(employee_service):
    count = 5 
    employee_service.dal.add_employee = MagicMock(return_value=5)
    mock_add_employee = employee_service.dal.add_employee
    employee_service.generate_random_employees(count)
    assert mock_add_employee.call_count == count


def test_generate_specific_employees(employee_service):
    count = 3 
    employee_service.dal.add_employee = MagicMock(return_value=3)
    mock_add_employee = employee_service.dal.add_employee
    employee_service.generate_specific_employees(count)
    assert mock_add_employee.call_count == count


def test_query_male_f_employees(employee_service):
    employee_service.query_male_f_employees()
    employee_service.dal.query_male_f_employees.assert_called_once()
    

def test_optimize_query_male_f_employees(employee_service):
     employee_service.optimize_and_query_male_f_employees()
     employee_service.dal.optimize_and_query_male_f_employees.assert_called_once()
