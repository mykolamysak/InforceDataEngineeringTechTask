import faker
import random
import csv
import pandas as pd
import re
from constants import CSV_FILE, UPDATED_CSV_FILE, NUM_RECORDS, EMAIL_DOMAINS

fake = faker.Faker()


class FileHandler:
    def __init__(self):
        self.file_path = CSV_FILE
        self.updated_file_path = UPDATED_CSV_FILE

    def read_csv_file(self):
        """Reads the CSV file using pandas"""
        return pd.read_csv(self.file_path)

    def write_csv_file(self, data_frame):
        """Writes the DataFrame to CSV"""
        data_frame.to_csv(self.updated_file_path, index=False)

    def generate_csv(self):
        """Generates CSV using built-in csv module"""
        with open(self.file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'name', 'email', 'signup_date'])

            for user_id in range(1, NUM_RECORDS + 1):
                name = fake.name()
                local_part = fake.user_name()
                domain = random.choice(EMAIL_DOMAINS)
                email = f"{local_part}@{domain}"
                signup_date = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([user_id, name, email, signup_date])

    def convert_signup_date_format(self, data_frame):
        """Converts time format using Pandas"""
        data_frame['signup_date'] = pd.to_datetime(data_frame['signup_date']).dt.strftime('%Y-%m-%d')
        return data_frame

    def filter_invalid_emails(self, data_frame):
        """Filter rows where the 'email' field matches the valid email pattern"""
        email_pattern = r"^\S+@\S+\.\S+$"
        data_frame = data_frame[data_frame['email'].apply(lambda x: re.match(email_pattern, x) is not None)]
        return data_frame

    def add_email_domain_column(self, data_frame):
        """Extracts the domain from email field and adds it as a column 'domain'"""
        data_frame['domain'] = data_frame['email'].apply(lambda x: x.split('@')[1])
        return data_frame
