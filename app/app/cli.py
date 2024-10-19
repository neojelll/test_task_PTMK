from main import create_connection, create_table, add_employee, list_employees, generate_random_employees, generate_specific_employees, query_male_f_employees, optimize_and_query_male_f_employees
from datetime import datetime
import time
import sys


def main():
    if len(sys.argv) < 2:
        print("Usage: myApp <mode> [parameters]")
        return
    mode = int(sys.argv[1])
    session = create_connection()
    if mode == 1:
        create_table(session)
        print("Table created.")  
    elif mode == 2:
        if len(sys.argv) != 5:
            print("Usage: myApp 2 <Full Name> <Birth Date> <Gender>")
            return
        full_name = sys.argv[2]
        birth_date = datetime.strptime(sys.argv[3], '%Y-%m-%d').date()
        gender = sys.argv[4]
        add_employee(session, full_name, birth_date, gender)
        print("Employee added.")   
    elif mode == 3:
        list_employees(session)
    elif mode == 4:
        generate_random_employees(session, 1000000)
        generate_specific_employees(session, 100)
        print("Employees generated.")
    elif mode == 5:
        start_time = time.time()
        query_male_f_employees(session)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time} seconds")
    elif mode == 6:
        start_time = time.time()
        optimize_and_query_male_f_employees(session)
        end_time = time.time()
        print("Optimization completed (implement as needed).")
        print(f"Execution time: {end_time - start_time} seconds")
    session.close()


if __name__ == "__main__":
    main()
