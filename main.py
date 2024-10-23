import re
import pandas as pd
import os


def read_csv_file(file_path):
    """Reads the .csv file"""
    return pd.read_csv(file_path)


def convert_signup_date_format(data_frame):
    """Converts time format using Pandas"""
    data_frame['signup_date'] = pd.to_datetime(data_frame['signup_date']).dt.strftime('%Y-%m-%d')
    return data_frame


def filter_invalid_emails(data_frame):
    """Filter rows where the 'email' field matches the valid email pattern"""
    # Email basic validation (source: https://uibakery.io/regex-library/email-regex-python)
    email_pattern = r"^\S+@\S+\.\S+$"
    data_frame = data_frame[data_frame['email'].apply(lambda x: re.match(email_pattern, x) is not None)]
    return data_frame


def add_email_domain_column(data_frame):
    """Extracts the domain from email field and adds it as a column 'domain'"""
    data_frame['domain'] = data_frame['email'].apply(lambda x: x.split('@')[1])
    return data_frame


if __name__ == "__main__":
    DIRECTORY = 'data'

    # Create folder
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)

    FILE_PATH = f'{DIRECTORY}/user_data.csv'
    UPDATED_FILE_PATH = f'{DIRECTORY}/updated_user_data.csv'

    data_frame = read_csv_file(FILE_PATH)

    data_frame = convert_signup_date_format(data_frame)
    data_frame = filter_invalid_emails(data_frame)
    data_frame = add_email_domain_column(data_frame)

    print(data_frame.head())
    data_frame.to_csv(UPDATED_FILE_PATH, index=False)
