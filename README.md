# SQL Query Generator

A simple Python tool that converts natural language English phrases into SQL queries for basic database operations.

## 🚀 Features

- Convert English sentences to SQL queries
- Support for basic SQL operations:
  - SELECT - retrieve data
  - INSERT - add new records
  - UPDATE - modify existing records
  - DELETE - remove records
- Custom database schema management
- Simple command-line interface
- No external dependencies - runs with standard Python

## 📋 Requirements

- Python 3.6 or higher

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sql-query-generator.git
cd sql-query-generator
```

2. No additional dependencies required - just run with Python!

## 🏃‍♂️ Usage

Run the program:
```bash
python main.py
```

### Example Queries

#### SELECT Queries:
- "Show all users"
- "Get name and email from users"
- "Find users where age is greater than 30"
- "Select products where category equals Electronics"

#### INSERT Queries:
- "Add user with values John, john@example.com, 25"
- "Insert product with name Laptop, price 999, category Electronics"

#### UPDATE Queries:
- "Update users set name to Alice where id equals 5"
- "Change product price to 45 where name equals Keyboard"

#### DELETE Queries:
- "Delete users where id equals 10"
- "Remove products where price is less than 10"

### Schema Management

Type `schema` at the prompt to:
- View current database schema
- Add or update tables and columns

Type `exit` to quit the program.

## 🌟 How It Works

The SQL Query Generator uses pattern matching and keyword recognition to:

1. Identify the query type (SELECT, INSERT, UPDATE, DELETE)
2. Extract table and column names
3. Parse conditions and values
4. Generate properly formatted SQL queries

## 📝 Example Session

```
SQL Query Generator
Enter 'exit' to quit
Enter 'schema' to view or update database schema

Enter your English query:
> show all users

Generated SQL Query:
SELECT * FROM users;

Enter your English query:
> find products where price is less than 50

Generated SQL Query:
SELECT * FROM products WHERE price < 50;

Enter your English query:
> add user with values John, john@example.com, 30

Generated SQL Query:
INSERT INTO users (name, email, age) VALUES ('John', 'john@example.com', 30);
```

## ⚠️ Limitations

- Only handles basic SQL operations
- No support for JOINs, GROUP BY, or complex conditions
- Limited natural language processing capabilities
- Not connected to any actual database (generates queries only)

## 🔍 Future Improvements

- Add support for more complex SQL features (JOINs, subqueries, etc.)
- Implement more sophisticated NLP for better query understanding
- Create a web interface for easier interaction
- Add database connection to execute the generated queries
- Implement validation to prevent SQL injection

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
