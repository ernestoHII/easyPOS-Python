import os
import pyodbc

def establish_db_connection():
    try:
        # Get database credentials from environment variables
        db_server = os.getenv("DB_SERVER")
        db_database = os.getenv("DB_DATABASE")
        db_username = os.getenv("DB_USERNAME")
        db_password = os.getenv("DB_PASSWORD")

        # Establish a connection to the database
        connection_string = f'DRIVER={{SQL Server}};SERVER={db_server};DATABASE={db_database};UID={db_username};PWD={db_password}'
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        return conn, cursor

    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None
