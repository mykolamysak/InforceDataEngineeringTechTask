import re
import pandas as pd


class DataProcessing:
    @staticmethod
    def convert_signup_date_format(data_frame):
        data_frame['signup_date'] = pd.to_datetime(data_frame['signup_date']).dt.strftime('%Y-%m-%d')
        return data_frame

    @staticmethod
    def filter_invalid_emails(data_frame):
        email_pattern = r"^\S+@\S+\.\S+$"
        data_frame = data_frame[data_frame['email'].apply(lambda x: re.match(email_pattern, x) is not None)]
        return data_frame

    @staticmethod
    def add_email_domain_column(data_frame):
        data_frame['domain'] = data_frame['email'].apply(lambda x: x.split('@')[1])
        return data_frame
