# SQL Query Generator
# This simple tool converts English phrases into SQL queries

import re
import json
import os

class SQLQueryGenerator:
    def __init__(self):
        # Define common keywords and patterns for SQL queries
        self.select_keywords = ["show", "display", "get", "find", "select", "retrieve", "list", "query"]
        self.insert_keywords = ["add", "insert", "create", "put", "include"]
        self.update_keywords = ["update", "modify", "change", "edit", "alter", "set"]
        self.delete_keywords = ["delete", "remove", "drop", "exclude", "eliminate"]
        
        # Load database schema information
        self.tables = self.load_schema()
    
    def load_schema(self):
        """
        Load database schema from schema.json if exists
        Otherwise, use a default schema for demonstration
        """
        if os.path.exists("schema.json"):
            with open("schema.json", "r") as f:
                return json.load(f)
        else:
            # Default schema for demonstration
            return {
                "users": ["id", "name", "email", "age", "created_at"],
                "products": ["id", "name", "price", "category", "description"],
                "orders": ["id", "user_id", "total", "status", "order_date"]
            }
    
    def save_schema(self):
        """Save the current schema to a json file"""
        with open("schema.json", "w") as f:
            json.dump(self.tables, f, indent=2)
    
    def identify_query_type(self, query):
        """Identify the type of SQL query based on the English phrase"""
        query = query.lower()
        
        # Identify query type based on keywords
        if any(keyword in query for keyword in self.select_keywords):
            return "SELECT"
        elif any(keyword in query for keyword in self.insert_keywords):
            return "INSERT"
        elif any(keyword in query for keyword in self.update_keywords):
            return "UPDATE"
        elif any(keyword in query for keyword in self.delete_keywords):
            return "DELETE"
        else:
            return "UNKNOWN"
    
    def identify_table(self, query):
        """Identify the table name from the English phrase"""
        for table in self.tables.keys():
            if table in query.lower() or table[:-1] in query.lower():  # Handle both singular and plural
                return table
        
        return None
    
    def identify_columns(self, query, table):
        """Identify columns mentioned in the query"""
        if not table or table not in self.tables:
            return []
        
        mentioned_columns = []
        query_lower = query.lower()
        
        for column in self.tables[table]:
            # Check if column is mentioned in the query
            if column in query_lower:
                mentioned_columns.append(column)
        
        return mentioned_columns
    
    def extract_conditions(self, query):
        """Extract condition values from the query"""
        conditions = []
        
        # Look for common condition patterns
        where_patterns = [
            r"where (\w+) (?:is|=|equals|equal to) (\w+|\d+|'[^']+'|\"[^\"]+\")",
            r"where (\w+) (?:>|greater than) (\d+)",
            r"where (\w+) (?:<|less than) (\d+)",
            r"where (\w+) like (\w+|\d+|'[^']+'|\"[^\"]+\")",
            r"where (\w+) in \(([^)]+)\)"
        ]
        
        for pattern in where_patterns:
            matches = re.finditer(pattern, query.lower())
            for match in matches:
                column = match.group(1)
                value = match.group(2)
                
                # Determine operator
                operator = "="
                if "greater than" in match.group(0) or ">" in match.group(0):
                    operator = ">"
                elif "less than" in match.group(0) or "<" in match.group(0):
                    operator = "<"
                elif "like" in match.group(0):
                    operator = "LIKE"
                elif "in" in match.group(0):
                    operator = "IN"
                
                # Add quotes if value is not a number and not already quoted
                if not value.isdigit() and not (value.startswith("'") and value.endswith("'")):
                    if not (value.startswith('"') and value.endswith('"')):
                        value = f"'{value}'"
                
                conditions.append((column, operator, value))
        
        return conditions
    
    def generate_select_query(self, query):
        """Generate a SELECT SQL query from the English phrase"""
        table = self.identify_table(query)
        if not table:
            return "ERROR: Could not identify table name in the query."
        
        columns = self.identify_columns(query, table)
        conditions = self.extract_conditions(query)
        
        # If no columns are specified, select all columns
        column_clause = ", ".join(columns) if columns else "*"
        
        # Create the basic SELECT query
        sql_query = f"SELECT {column_clause} FROM {table}"
        
        # Add WHERE clause if there are conditions
        if conditions:
            where_clause = " AND ".join([f"{column} {operator} {value}" for column, operator, value in conditions])
            sql_query += f" WHERE {where_clause}"
        
        return sql_query + ";"
    
    def generate_insert_query(self, query):
        """Generate an INSERT SQL query from the English phrase"""
        table = self.identify_table(query)
        if not table:
            return "ERROR: Could not identify table name in the query."
        
        # Look for values to insert
        # This is a simplified version - a complete solution would need to parse more complex patterns
        values_pattern = r"values?\s*(?:\(|:)?\s*([^)]+)(?:\))?"
        match = re.search(values_pattern, query.lower())
        
        if not match:
            return "ERROR: Could not identify values to insert."
        
        # Process the values
        value_text = match.group(1)
        values = [val.strip() for val in value_text.split(",")]
        
        # Identify which columns to use
        columns = self.identify_columns(query, table)
        if not columns:
            # Use default columns from schema (excluding id if it exists)
            columns = [col for col in self.tables[table] if col != "id"]
        
        # Format values correctly
        formatted_values = []
        for value in values:
            if value.isdigit():
                formatted_values.append(value)
            else:
                # Add quotes if not already quoted
                if not (value.startswith("'") and value.endswith("'")):
                    if not (value.startswith('"') and value.endswith('"')):
                        value = f"'{value}'"
                formatted_values.append(value)
        
        # Create the INSERT query
        columns_clause = ", ".join(columns)
        values_clause = ", ".join(formatted_values)
        
        return f"INSERT INTO {table} ({columns_clause}) VALUES ({values_clause});"
    
    def generate_update_query(self, query):
        """Generate an UPDATE SQL query from the English phrase"""
        table = self.identify_table(query)
        if not table:
            return "ERROR: Could not identify table name in the query."
        
        # Look for SET patterns (simplified)
        set_pattern = r"set (\w+) to (\w+|\d+|'[^']+'|\"[^\"]+\")"
        set_matches = re.finditer(set_pattern, query.lower())
        
        set_clauses = []
        for match in set_matches:
            column = match.group(1)
            value = match.group(2)
            
            # Add quotes if value is not a number and not already quoted
            if not value.isdigit() and not (value.startswith("'") and value.endswith("'")):
                if not (value.startswith('"') and value.endswith('"')):
                    value = f"'{value}'"
            
            set_clauses.append(f"{column} = {value}")
        
        if not set_clauses:
            return "ERROR: Could not identify values to update."
        
        # Extract conditions
        conditions = self.extract_conditions(query)
        
        # Create the UPDATE query
        sql_query = f"UPDATE {table} SET " + ", ".join(set_clauses)
        
        # Add WHERE clause if there are conditions
        if conditions:
            where_clause = " AND ".join([f"{column} {operator} {value}" for column, operator, value in conditions])
            sql_query += f" WHERE {where_clause}"
        
        return sql_query + ";"
    
    def generate_delete_query(self, query):
        """Generate a DELETE SQL query from the English phrase"""
        table = self.identify_table(query)
        if not table:
            return "ERROR: Could not identify table name in the query."
        
        # Extract conditions
        conditions = self.extract_conditions(query)
        
        # Create the DELETE query
        sql_query = f"DELETE FROM {table}"
        
        # Add WHERE clause if there are conditions
        if conditions:
            where_clause = " AND ".join([f"{column} {operator} {value}" for column, operator, value in conditions])
            sql_query += f" WHERE {where_clause}"
        else:
            # Safety check - confirm with user before deleting all records
            return "WARNING: This query would delete all records from the table. Please specify conditions."
        
        return sql_query + ";"
    
    def generate_query(self, english_query):
        """Generate a SQL query from an English phrase"""
        query_type = self.identify_query_type(english_query)
        
        if query_type == "SELECT":
            return self.generate_select_query(english_query)
        elif query_type == "INSERT":
            return self.generate_insert_query(english_query)
        elif query_type == "UPDATE":
            return self.generate_update_query(english_query)
        elif query_type == "DELETE":
            return self.generate_delete_query(english_query)
        else:
            return "Sorry, I couldn't understand the type of query you want to create."

# Function to create a simple CLI interface
def main():
    generator = SQLQueryGenerator()
    
    print("SQL Query Generator")
    print("Enter 'exit' to quit")
    print("Enter 'schema' to view or update database schema")
    
    while True:
        print("\nEnter your English query:")
        user_input = input("> ")
        
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        
        elif user_input.lower() == 'schema':
            print("\nCurrent Schema:")
            for table, columns in generator.tables.items():
                print(f"{table}: {', '.join(columns)}")
            
            update = input("\nWould you like to update the schema? (yes/no): ")
            if update.lower() == 'yes':
                table_name = input("Enter table name: ")
                columns = input("Enter column names (comma separated): ")
                column_list = [col.strip() for col in columns.split(",")]
                generator.tables[table_name] = column_list
                generator.save_schema()
                print("Schema updated successfully!")
        
        else:
            result = generator.generate_query(user_input)
            print("\nGenerated SQL Query:")
            print(result)

if __name__ == "__main__":
    main()