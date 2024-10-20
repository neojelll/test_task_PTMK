from datetime import datetime
from .service import EmployeeService
import argparse
import time


def main():
    service = EmployeeService()
    
    parser = argparse.ArgumentParser(description="Employee Management Application")
    subparsers = parser.add_subparsers(dest='mode', required=True)

    parser_create = subparsers.add_parser('create', help='Create employee table')

    parser_add = subparsers.add_parser('add', help='Add an employee')
    parser_add.add_argument('full_name', type=str, help='Full name of the employee')
    parser_add.add_argument('birth_date', type=str, help='Birth date of the employee (YYYY-MM-DD)')
    parser_add.add_argument('gender', type=str, help='Gender of the employee')

    parser_list = subparsers.add_parser('list', help='List all employees')

    parser_generate = subparsers.add_parser('generate', help='Generate test employees')

    parser_query_male = subparsers.add_parser('query_male', help='Query male employees')

    parser_optimize_query = subparsers.add_parser('optimize_query', help='Optimize and query male employees')

    args = parser.parse_args()

    if args.mode == 'create':
        service.create_table()
        print("Table created.")
    
    elif args.mode == 'add':
        birth_date = datetime.strptime(args.birth_date, '%Y-%m-%d').date()
        service.add_employee(args.full_name, birth_date, args.gender)
        print("Employee added.")
    
    elif args.mode == 'list':
        service.list_employees()
    
    elif args.mode == 'generate':
        service.generate_random_employees(1000000)
        service.generate_specific_employees(100)
        print("Employees generated.")
    
    elif args.mode == 'query_male':
        start_time = time.time()
        service.query_male_f_employees()
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
    
    elif args.mode == 'optimize_query':
        start_time = time.time()
        service.optimize_and_query_male_f_employees()
        end_time = time.time()
        print("Optimization completed.")
        print(f"Execution time: {end_time - start_time} seconds")

    service.dal.session.close()


if __name__ == "__main__":
    main()
