import os
import pymysql
import pandas as pd

# Database connection
connection = pymysql.connect(
    host=os.environ['BWW_DB_HOST'] or 'localhost',
    user=os.environ['BWW_DB_USER'],
    password=os.environ['BWW_DB_PASSWD'],
    database=os.environ['BWW_DB_NAME'] or 'BerginWoodWorking'
)

# Load the CSV file
df = pd.read_csv('../data/encoded_images.csv')

# Insert data into the MySQL table
try:
    with connection.cursor() as cursor:
        for index, row in df.iterrows():
            sql = """
            INSERT INTO product_images (sku, project_name, encoded_photo) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (row['SKU'], row['Project_Name'], row['Encoded_Photo']))
        connection.commit()
finally:
    connection.close()
