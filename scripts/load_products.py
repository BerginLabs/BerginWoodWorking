#!/usr/bin/env python3

import os
import csv

import pandas as pd
from sqlalchemy import create_engine


def refactor_csv_headers(input_file, output_file):
    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader)
        
        headers = [header.replace(' ', '_').lower() for header in headers]
        headers = [header.strip("#") for header in headers]
        
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(headers)
            
            for row in reader:
                row = [cell.strip("$ ").strip(" ") for cell in row]
                writer.writerow(row)


def load_data(csv_file):
    db_config = {
        'user': os.environ['BWW_DB_USER'],
        'password': os.environ['BWW_DB_PASSWD'],
        'host': os.environ['BWW_DB_HOST'] or 'localhost',
        'database': os.environ['BWW_DB_NAME'] or 'BerginWoodWorking'
    }

    db_url = f"mysql+mysqldb://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
    engine = create_engine(db_url)

    df = pd.read_csv(csv_file)
    df.columns = [col.replace(' ', '_').lower() for col in df.columns]

    df.to_sql(name='products', con=engine, if_exists='replace', index=False)
    return



if __name__ == '__main__':
    input_file  = os.path.join('..', 'data', 'products_updated.csv')
    output_file = os.path.join('..', 'data', 'products_refactored.csv')

    if os.path.exists(output_file):
        os.remove(output_file)

    refactor_csv_headers(input_file, output_file)
    load_data(output_file)
