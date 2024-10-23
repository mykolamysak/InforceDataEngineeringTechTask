import os
import psycopg2
import configparser
from tabulate import tabulate


def read_db_config(config_file='config.ini', section='database'):
    """Reads database config"""
    parser = configparser.ConfigParser()
    parser.read(config_file)

    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {config_file} file')

    return db_config


def execute_query_from_file(file_path, db_config):
    """Executes SQL query from file"""
    try:
        # Connect to DB
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        # Read query from file
        with open(file_path, 'r') as file:
            sql_query = file.read()

        # Output
        print("\nQuery processing:")
        print(sql_query)

        # Execution
        cursor.execute(sql_query)

        # If there is 'SELECT'
        if sql_query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            print("\nrResults:")
            print(tabulate(results, headers=columns, tablefmt='psql'))

        # If not: just commit
        else:
            conn.commit()
            print(f"Query from {file_path} executed successfully!")

    except Exception as e:
        print(f"Error occured while executing query from {file_path}: {e}")

    finally:
        # Close anyway
        cursor.close()
        conn.close()


def list_and_select_query(folder_path):
    """Outputs list of queries"""
    while True:
        # Get list
        sql_files = [f for f in os.listdir(folder_path) if f.endswith(".sql")]

        if not sql_files:
            print("There is no SQL files in the folder.")
            return None

        print("\nAvailable SQL files:")
        for idx, file in enumerate(sql_files, start=1):
            print(f"{idx}. {file}")

        try:
            choice = int(input("\nEnter number of the file to execute(0 for exit): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(sql_files):
                return os.path.join(folder_path, sql_files[choice - 1])
            else:
                print(f"Please, choose number between 1 and {len(sql_files)}.")
        except ValueError:
            print("There is no such number.")


if __name__ == "__main__":
    folder_path = 'queries'  # Queries folder
    db_config = read_db_config()

    # Infinity loop menu
    while True:
        selected_query_file = list_and_select_query(folder_path)
        if selected_query_file:
            execute_query_from_file(selected_query_file, db_config)
        else:
            break
