CREATE TABLE employees (
	id SERIAL PRIMARY KEY,
	full_name VARCHAR(100) NOT NULL,
	birth_date DATE NOT NULL,
	gender VARCHAR(6) NOT NULL
);