from file_handler import FileHandler
from data_processing import DataProcessing
from sql_handler import SqlHandler
from pathlib import Path


def file_menu(file_handler, data_processing):
    print("\nFile Menu:")
    print("1. Generate Data")
    print("2. Modify Data")
    print("3. Return to Main Menu")

    choice = input("Choose an option (1, 2, or 3): ")

    match choice:
        case "1":
            generate_data(file_handler)
        case "2":
            modify_data(file_handler, data_processing)
        case "3":
            return
        case _:
            print("Invalid option. Please try again.")
            file_menu(file_handler, data_processing)


def generate_data(file_handler):
    print("\nGenerating data...")
    file_handler.generate_csv()
    print("Data generated successfully.")


def modify_data(file_handler, data_processing):
    print("\nModifying data...")
    data_frame = file_handler.read_csv_file()

    # Call methods from DataProcessing class
    data_frame = data_processing.convert_signup_date_format(data_frame)
    data_frame = data_processing.filter_invalid_emails(data_frame)
    data_frame = data_processing.add_email_domain_column(data_frame)

    file_handler.write_csv_file(data_frame)
    print("Data modified and saved successfully.")


def sql_menu(sql_handler):
    sql_file = list_and_select_query()
    if sql_file:
        sql_handler.execute_query_from_file(sql_file)


def list_and_select_query():
    current_dir = Path(__file__).resolve().parent
    sql_folder = current_dir.parent / 'sql'

    if not sql_folder.exists():
        print(f"SQL folder not found at {sql_folder}")
        return

    sql_files = [f for f in sql_folder.iterdir() if f.suffix == '.sql']

    if not sql_files:
        print("No SQL files found in the folder.")
        return

    print("\nAvailable SQL files:")
    for idx, file in enumerate(sql_files, start=1):
        print(f"{idx}. {file.name}")

    while True:
        try:
            choice = int(input("\nEnter number of the file to execute (0 to exit): "))
            if choice == 0:
                return
            if 1 <= choice <= len(sql_files):
                return sql_files[choice - 1]
            else:
                print(f"Please choose a number between 1 and {len(sql_files)}.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. File Handling")
        print("2. SQL Queries")
        print("3. Exit")

        choice = input("Choose an option (1, 2, or 3): ")
        match choice:
            case "1":
                file_menu(file_handler, data_processing)
            case "2":
                sql_menu(sql_handler)
            case "3":
                print("Exiting the program.")
                return
            case _:
                print("Invalid option. Please try again.")


if __name__ == "__main__":
    sql_handler = SqlHandler()
    file_handler = FileHandler()
    data_processing = DataProcessing()
    main_menu()
