from datetime import datetime
from .service import EmployeeService
from .logger import configure_logger
from loguru import logger
import argparse


configure_logger()


def main():
    service = EmployeeService()

    parser = argparse.ArgumentParser(description="Employee Management Application")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    subparsers.add_parser("1", help="Create employee table")

    parser_add = subparsers.add_parser("2", help="Add an employee")
    parser_add.add_argument("full_name", type=str, help="Full name of the employee")
    parser_add.add_argument(
        "birth_date", type=str, help="Birth date of the employee (YYYY-MM-DD)"
    )
    parser_add.add_argument("gender", type=str, help="Gender of the employee")

    subparsers.add_parser("3", help="List all employees")

    subparsers.add_parser("4", help="Generate test employees")

    subparsers.add_parser("5", help="Query male employees")

    subparsers.add_parser("6", help="Optimize and query male employees")

    args = parser.parse_args()

    if args.mode == "1":
        service.create_table()
        logger.debug("Table created.")

    elif args.mode == "2":
        birth_date = datetime.strptime(args.birth_date, "%Y-%m-%d").date()
        service.add_employee(args.full_name, birth_date, args.gender)
        logger.debug("Employee added.")

    elif args.mode == "3":
        service.list_employees()

    elif args.mode == "4":
        service.generate_random_employees(1000000)
        service.generate_specific_employees(100)
        logger.debug("Employees generated.")

    elif args.mode == "5":
        service.query_male_f_employees()

    elif args.mode == "6":
        service.optimize_and_query_male_f_employees()

    service.dal.session.close()


if __name__ == "__main__":
    main()
