import psycopg2
import json
import boto3

# Define your PostgreSQL connection parameters
conn_params = {
    'dbname': 'your_database',
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'port': 'your_port'
}

# Define a dictionary of tables and columns to retrieve
tables_and_columns = {
    'table1': ['column1', 'column2'],
    'table2': ['column3', 'column4']
}

# Connect to PostgreSQL
conn = psycopg2.connect(**conn_params)

# Create a cursor
cursor = conn.cursor()

# Define a function to fetch data for each table and column
def fetch_data(table, columns):
    query = f"SELECT {', '.join(columns)} FROM {table}"
    cursor.execute(query)
    data = cursor.fetchall()
    return data, len(data)

# Initialize report dictionary
report = {'tables': {}}

# Iterate over the tables_and_columns dictionary
for table, columns in tables_and_columns.items():
    data, row_count = fetch_data(table, columns)
    report['tables'][table] = {
        'columns': columns,
        'row_count': row_count,
        'data': []
    }
    for row in data:
        report['tables'][table]['data'].append(dict(zip(columns, row)))

# Close cursor and connection
cursor.close()
conn.close()

# Write the data to a JSON file
with open('data.json', 'w') as json_file:
    json.dump(report, json_file, indent=4)

# Upload JSON file to S3
s3 = boto3.client('s3')
bucket_name = 'your_bucket_name'
s3_key = 'path/to/your/file/data.json'
with open('data.json', 'rb') as data_file:
    s3.upload_fileobj(data_file, bucket_name, s3_key)

# Generate report
print("Execution Report:")
for table, info in report['tables'].items():
    print(f"Table: {table}")
    print(f"Columns: {', '.join(info['columns'])}")
    print(f"Row Count: {info['row_count']}")
    print()

print(f"JSON file uploaded to S3 path: s3://{bucket_name}/{s3_key}")
