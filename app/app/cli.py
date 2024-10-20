from datetime import datetime
from .service import EmployeeService
import argparse
import time


def main():
    service = EmployeeService()

    parser = argparse.ArgumentParser(description="Employee Management Application")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    create_parser = subparsers.add_parser("1", help="Create employee table")
    create_parser.add_argument(
        "--alias", choices=["create"], help="Alias for create command"
    )

    parser_add = subparsers.add_parser("2", help="Add an employee")
    parser_add.add_argument("--alias", choices=["add"], help="Alias for add employee")
    parser_add.add_argument("full_name", type=str, help="Full name of the employee")
    parser_add.add_argument(
        "birth_date", type=str, help="Birth date of the employee (YYYY-MM-DD)"
    )
    parser_add.add_argument("gender", type=str, help="Gender of the employee")

    list_parser = subparsers.add_parser("3", help="List all employees")
    list_parser.add_argument("--alias", choices=["list"], help="Alias for list command")

    generate_parser = subparsers.add_parser("4", help="Generate test employees")
    generate_parser.add_argument(
        "--alias", choices=["generate"], help="Alias for generate command"
    )

    query_male_parser = subparsers.add_parser("5", help="Query male employees")
    query_male_parser.add_argument(
        "--alias", choices=["query_male"], help="Alias for query male command"
    )

    optimize_parser = subparsers.add_parser(
        "6", help="Optimize and query male employees"
    )
    optimize_parser.add_argument(
        "--alias", choices=["optimize_query"], help="Alias for optimize query command"
    )

    args = parser.parse_args()

    if args.mode in ["1", "create"]:
        service.create_table()
        print("Table created.")

    elif args.mode in ["2", "add"]:
        birth_date = datetime.strptime(args.birth_date, "%Y-%m-%d").date()
        service.add_employee(args.full_name, birth_date, args.gender)
        print("Employee added.")

    elif args.mode in ["3", "list"]:
        service.list_employees()

    elif args.mode in ["4", "generate"]:
        service.generate_random_employees(1000000)
        service.generate_specific_employees(100)
        print("Employees generated.")

    elif args.mode in ["5", "query_male"]:
        start_time = time.time()
        service.query_male_f_employees()
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")

    elif args.mode in ["6", "optimize_query"]:
        start_time = time.time()
        service.optimize_and_query_male_f_employees()
        end_time = time.time()
        print("Optimization completed.")
        print(f"Execution time: {end_time - start_time} seconds")

    service.dal.session.close()


if __name__ == "__main__":
    main()
