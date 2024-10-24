import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from constants import DB_CONFIG_FILE, DB_SECTION, SQL_FOLDER_PATH
import configparser
from tabulate import tabulate


class SqlHandler:
    def __init__(self):
        self.db_config = self.read_db_config()
        self.engine = create_engine(
            f"postgresql://{self.db_config['user']}"
            f":{self.db_config['password']}"
            f"@{self.db_config['host']}"
            f"/{self.db_config['dbname']}")
        self.Session = sessionmaker(bind=self.engine)

    def read_db_config(self):
        """Reads database configuration"""
        parser = configparser.ConfigParser()
        parser.read(DB_CONFIG_FILE)
        db_config = {}
        if parser.has_section(DB_SECTION):
            params = parser.items(DB_SECTION)
            for param in params:
                db_config[param[0]] = param[1]
        else:
            raise Exception(f'Section {DB_SECTION} not found in {DB_CONFIG_FILE}')

        # Check for required keys
        required_keys = ['user', 'password', 'host', 'dbname']
        for key in required_keys:
            if key not in db_config:
                raise KeyError(f"Missing '{key}' in the database configuration")

        return db_config

    def execute_query_from_file(self, file_path):
        """Executes SQL query from a file and prints the result using tabulate lib"""
        try:
            with open(file_path, 'r') as file:
                sql_query = file.read()

            with self.engine.connect() as connection:
                result = connection.execute(text(sql_query))
                if sql_query.strip().upper().startswith("SELECT"):
                    rows = result.fetchall()
                    if rows:
                        # Get column names from cursor
                        columns = result.keys()
                        # Print results using tabulate
                        print("\nQuery Result:")
                        print(tabulate(rows, headers=columns, tablefmt='psql'))
                    else:
                        print("No rows returned.")
                else:
                    connection.commit()
                    print(f"Query from {file_path} executed successfully!")
        except Exception as e:
            print(f"Error while executing query from {file_path}: {e}")

    def list_and_select_query(self, folder_path=SQL_FOLDER_PATH):
        """Outputs list of SQL files and allows the user to select one"""
        sql_files = [f for f in os.listdir(folder_path) if f.endswith(".sql")]

        if not sql_files:
            print("No SQL files found in the folder.")
            return None

        print("\nAvailable SQL files:")
        for idx, file in enumerate(sql_files, start=1):
            print(f"{idx}. {file}")

        while True:
            try:
                choice = int(input("\nEnter number of the file to execute (0 to exit): "))
                if choice == 0:
                    return None
                if 1 <= choice <= len(sql_files):
                    return os.path.join(folder_path, sql_files[choice - 1])
                else:
                    print(f"Please choose a number between 1 and {len(sql_files)}.")
            except ValueError:
                print("Invalid input. Please enter a number.")
