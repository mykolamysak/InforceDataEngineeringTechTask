import os
from pathlib import Path
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from tabulate import tabulate


class SqlHandler:
    def __init__(self):
        current_dir = Path(__file__).resolve().parent
        config_path = current_dir.parent / 'config.env'

        # Load environment variables from config file
        if not load_dotenv(config_path):
            raise EnvironmentError(f"Could not load config file at {config_path}")

        # Get required environment variables
        required_vars = ['DB_USER', 'DB_PASSWORD', 'DB_HOST', 'DB_PORT', 'DB_NAME']
        config = {}

        for var in required_vars:
            value = os.getenv(var)
            if value is None:
                raise EnvironmentError(f"Missing required environment variable: {var}")
            config[var] = value

        # Validate port is numeric
        try:
            int(config['DB_PORT'])
        except ValueError:
            raise EnvironmentError(f"DB_PORT must be a number, got: {config['DB_PORT']}")

        # Create database URL
        db_url = (
            f"postgresql://{config['DB_USER']}"
            f":{config['DB_PASSWORD']}"
            f"@{config['DB_HOST']}"
            f":{config['DB_PORT']}"
            f"/{config['DB_NAME']}"
        )

        self.engine = create_engine(db_url)
        self.session = sessionmaker(bind=self.engine)

    def execute_query_from_file(self, file_path):
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
                        print("\nQuery Result:")
                        print(tabulate(rows, headers=columns, tablefmt='psql'))
                    else:
                        print("No rows returned.")
                else:
                    connection.commit()
                    print(f"Query from {file_path} executed successfully!")
        except Exception as e:
            print(f"Error while executing query from {file_path}: {e}")

