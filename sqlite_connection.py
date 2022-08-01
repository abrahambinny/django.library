import sqlite3
import csv
import re
from datetime import datetime

db_name = 'db.sqlite3'

db_mapping = {
    'authors':
        {
            'table_name': 'inventory_authors',
            'column_name': 'name',
            'created_column': 'created_time',
            'modified_column': 'updated_time',
            'row_num': 2,
        },
    'language':
        {
            'table_name': 'inventory_language',
            'column_name': 'language',
            'created_column': 'created_time',
            'modified_column': 'updated_time',
            'row_num': 5,
            'data_list': ['eng', 'en-US', 'en-CA']
        },
    'book':
        {
            'table_name': 'inventory_book',
            'column_name': 'title',
            'created_column': 'created_time',
            'modified_column': 'updated_time',
        },
    
}


def db_conn(db_query):

    try:
        sqliteConnection = sqlite3.connect(db_name)
        cursor = sqliteConnection.cursor()
        print("Database Successfully Connected to SQLite")
        cursor.execute(db_query)
        sqliteConnection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        

def generate_data(csv_file, data_type):

    field_map = db_mapping[data_type]
    created_date = datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")
    
    if data_type == 'language':
        
        for item in field_map['data_list']:
        
            sql_query = f"INSERT INTO {field_map['table_name']} ({field_map['column_name']}, {field_map['created_column']}, {field_map['modified_column']}) VALUES ('{item.strip()}','{created_date}','{created_date}');"
            insert_data(sql_query)
        
    else:
        
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                sql_query = f"INSERT INTO {field_map['table_name']} ('book_id', 'isbn', 'available', 'author', 'pub_year', 'title', 'language', 'created_time', 'updated_time') VALUES ({refine_data(row[0])}, '{refine_data(row[1])}', True, '{refine_data(row[2])}', {refine_data(row[3])}, '{refine_data(row[4])}', '{refine_data(row[5])}','{created_date}','{created_date}');"
                insert_data(sql_query)
          
def refine_data(data):
    return bytes(data, 'utf-8').decode('utf-8','ignore')
                    
def insert_data(sql_query):
    
    print(sql_query)
    try:
        db_conn(sql_query)
    except Exception as e:
        print(f"Insertion Error: {str(e)}")



if __name__ == "__main__":
    
    generate_data("Backend_Data.csv", 'book')