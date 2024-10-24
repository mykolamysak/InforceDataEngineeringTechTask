from file_handler import FileHandler
from sql_handler import SqlHandler


def file_menu(file_handler):
    """File Handling Menu"""
    print("\nFile Menu:")
    print("1. Generate Data")
    print("2. Modify Data")
    print("3. Return to Main Menu")

    choice = input("Choose an option (1, 2, or 3): ")

    match choice:
        case "1":
            generate_data(file_handler)
        case "2":
            modify_data(file_handler)
        case "3":
            return
        case _:
            print("Invalid option. Please try again.")
            file_menu(file_handler)


def generate_data(file_handler):
    print("\nGenerating data...")
    file_handler.generate_csv()
    print("Data generated successfully.")


def modify_data(file_handler):
    print("\nModifying data...")
    data_frame = file_handler.read_csv_file()
    data_frame = file_handler.convert_signup_date_format(data_frame)
    data_frame = file_handler.filter_invalid_emails(data_frame)
    data_frame = file_handler.add_email_domain_column(data_frame)
    file_handler.write_csv_file(data_frame)
    print("Data modified and saved successfully.")


def sql_menu(sql_handler):
    """SQL Queries Menu"""
    sql_file = sql_handler.list_and_select_query()
    if sql_file:
        sql_handler.execute_query_from_file(sql_file)


def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. File Handling")
        print("2. SQL Queries")
        print("3. Exit")

        choice = input("Choose an option (1, 2, or 3): ")
        match choice:
            case "1":
                file_menu(file_handler)
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
    main_menu()
