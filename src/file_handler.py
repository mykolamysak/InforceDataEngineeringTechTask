import faker
import random
import csv
import pandas as pd
from settings import NUM_RECORDS, EMAIL_DOMAINS
from paths import CSV_FILE, UPDATED_CSV_FILE

fake = faker.Faker()


class FileHandler:
    @staticmethod
    def read_csv_file():
        return pd.read_csv(CSV_FILE)

    @staticmethod
    def write_csv_file(data_frame):
        data_frame.to_csv(UPDATED_CSV_FILE, index=False)

    @staticmethod
    def generate_csv():
        with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user_id', 'name', 'email', 'signup_date'])

            for user_id in range(1, NUM_RECORDS + 1):
                name = fake.name()
                local_part = fake.user_name()
                domain = random.choice(EMAIL_DOMAINS)
                email = f"{local_part}@{domain}"
                signup_date = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')
                writer.writerow([user_id, name, email, signup_date])
