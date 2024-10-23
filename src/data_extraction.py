import csv
import faker  # generates names, emails, etc
import pandas as pd
import random
import os

fake = faker.Faker()

NUM_RECORDS = 1001
DIRECTORY = 'data'
FILENAME = f'{DIRECTORY}/user_data.csv'

# Create folder
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY)

# Email domains
custom_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'ukr.net', 'mailbox.org', 'example.io']

# Generate CSV
with open(FILENAME, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['user_id', 'name', 'email', 'signup_date'])

    for user_id in range(1, NUM_RECORDS + 1):
        name = fake.name()

        # Email generation
        local_part = fake.user_name()
        domain = random.choice(custom_domains)
        email = f"{local_part}@{domain}"

        signup_date = fake.date_time_this_decade().strftime('%Y-%m-%d %H:%M:%S')

        writer.writerow([user_id, name, email, signup_date])

# Read from CSV
df = pd.read_csv(FILENAME)
print(df.head())
