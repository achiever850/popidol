# Import necessary libraries and modules for AWS Glue, PySpark, and HTTP requests processing
from awsglue.dynamicframe import DynamicFrame
import requests
import sys
from pyspark.sql import SparkSession
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext  # Note: Corrected capitalization
from pyspark.sql.functions import udf, col, lit
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, BooleanType, ArrayType, MapType, IntegerType  # Note: Corrected capitalization
from pyspark.sql.functions import to_timestamp, regexp_replace, when, concat

from awsglue.context import GlueContext
from awsglue.job import Job

# Retrieve job parameters from AWS Glue's job configuration
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)  # Note: Variable naming convention corrected
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# API base URL and key for authentication
base_api_url = "https://developer.usastaffing.gov"
api_key = '6wswmzc1h11900nmchucelfnwegreufhewheerggggb'

# Headers for HTTP requests to the API
headers = {
    'Api_Key': api_key
}

# Configuration options for Redshift connection
my_conn_options = {
    "dbtable": "prakash_csv_test.Announcements",
    "database": "hcd-dev-db"
}

def extract_id_from_links(links, rel_value):
    """
    Extracts a specific ID from a list of link objects based on a relation value.

    Args:
        links (list): A list of link objects.
        rel_value (str): The relation value to identify the correct link object.

    Returns:
        str: The extracted ID or None if not found or an error occurs.
    """
    print("inside udf")
    for link in links:
        if link['rel'] == rel_value:
            try:
                val = link['href'].split('/')[3]
                res = val.split('|')[-1]
                return res
            except Exception as e:
                print(link['href'])
                print(e)
                return None
    return None

class ReadAPI:
    """
    A class to read data from an API, process it, and handle pagination.
    """
    def __init__(self, app_name, table_schema, timestamp_col_li):
        """
        Initializes the ReadAPI object with application name, table schema, and timestamp columns.

        Args:
            app_name (str): Name of the application to fetch data for.
            table_schema (StructType): Schema definition for the data to be processed.
            timestamp_col_li (list): List of columns that contain timestamp information.
        """
        self.app_name = app_name
        self.headers = headers
        self.table_schema = table_schema
        self.timestamp_columns = timestamp_col_li
        self.api_url = base_api_url + "/api/" + app_name

    def convert_raw_list_to_df(self, raw_api_data_list):
        """
        Converts a list of raw API data into a Spark DataFrame using the specified schema.

        Args:
            raw_api_data_list (list): The list of raw data to be converted.

        Returns:
            DataFrame: A Spark DataFrame containing the processed data.
        """
        df = spark.createDataFrame(raw_api_data_list, schema=self.table_schema)
        return df

    def fetch_api_data(self, api_url):
        """
        Fetches data from the API at the specified URL.

        Args:
            api_url (str): The URL to fetch the data from.

        Returns:
            dict: The JSON response from the API or None if an error occurs.
        """
        try:
            response = requests.get(api_url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(e)
            return None

    def handle_pagination(self, raw_api_data):
        """
        Handles pagination by extracting metadata from the API response.

        Args:
            raw_api_data (dict): The raw API data containing pagination information.
        """
        page_dict = raw_api_data['paging']
        self.total_count = page_dict['metadata']['totalcount']
        self.page_size = page_dict['metadata']['pagesize']
        self.current_page = page_dict['metadata']['currentpage']
        self.total_pages = page_dict['metadata']['totalpages']
        self.snapshot = page_dict['metadata']['snapshot']
        self.previous = page_dict['previous']
        self.next_api_url = page_dict['next']

    def extract_links_rel_list(self, raw_api_data):
        """
        Extracts a list of relation values from the link objects in the API data.

        Args:
            raw_api_data (dict): The raw API data.
        """
        link_li = raw_api_data['data'][0]['_links']
        self.links_rel_list = [ele['rel'] for ele in link_li if ele['rel'] != 'self']

    def concat_df(self, new_df):
        """
        Concatenates a new DataFrame with the existing DataFrame.

        Args:
            new_df (DataFrame): The new DataFrame to concatenate.
        """
        self.df = self.df.union(new_df)
        print("concatenating with new df")

    def process_data_for_all_pages(self):
        """
        Processes API data for all pages by fetching and concatenating each page's data.
        """
        for i in range(2, self.total_pages + 1):
            print(self.next_api_url)
            raw_api_data = self.fetch_api_data(base_api_url + self.next_api_url)
            if raw_api_data:
                self.handle_pagination(raw_api_data)
                raw_api_data_list = raw_api_data['data']
                new_df = self.convert_raw_list_to_df(raw_api_data_list)
                self.concat_df(new_df)

    def handle_links(self):
        """
        Processes link objects to extract IDs and convert them into DataFrame columns.
        """
        df = self.df
        print("::: the rel list :::")
        print(self.links_rel_list)
        for rel_value in self.links_rel_list:
            print(f"Extracting for: {rel_value}")
            df = df.withColumn(rel_value, lit(extract_id_from_links(col("_links"), lit(rel_value))).cast(IntegerType()))
            print("converting json to text object")
            df = df.withColumn('_links', col('_links').cast(StringType()))
            self.df = df

    def handle_timestamp_columns(self):
        """
        Processes timestamp columns to ensure they are in the correct format.
        """
        for column in self.timestamp_columns:
            self.df = self.df.withColumn(column, when(~col(column).contains('.'), concat(col(column), lit('.000'))).otherwise(col(column)))
            self.df = self.df.withColumn(column, to_timestamp(col(column), "yyyy-MM-dd'T'HH:mm:ss.SSSSSSSSS"))

    def execute(self):
        """
        Executes the process to fetch, process, and prepare API data for storage.

        Returns:
            DataFrame: The final processed Spark DataFrame ready for storage.
        """
        # First time operation
        raw_api_data = self.fetch_api_data(self.api_url)
        if raw_api_data:
            self.handle_pagination(raw_api_data)
            raw_api_data_list = raw_api_data['data']
            self.df = self.convert_raw_list_to_df(raw_api_data_list)
            if self.total_pages > 1:
                self.process_data_for_all_pages()
                self.extract_links_rel_list(raw_api_data)
                self.handle_links()
                self.handle_timestamp_columns()
                self.df = self.df.drop('_links')
                return self.df

def write_to_redshift(glueContext, input_dynamic_frame):
    """
    Writes the processed data to Redshift using the specified Glue context and DynamicFrame.

    Args:
        glueContext (GlueContext): The Glue context to use for the operation.
        input_dynamic_frame (DynamicFrame): The DynamicFrame containing the data to write.
    """
    glueContext.write_dynamic_frame.from_jdbc_conf(
        frame=input_dynamic_frame,
        catalog_connection="Redshift connection_hcd_dev-db",
        connection_options=my_conn_options,
        redshift_tmp_dir="s3://aws-glue-assets-094737541415-us-gov-west-1/temporary/")

# Main execution flow
appname = "applications"
import map_schema

# Retrieve schema and timestamp column information based on the application name
table_schema_param = appname + "_schema"
datetime_cols_param = appname + "_timestamp_columns"

table_schema = getattr(map_schema, table_schema_param)
timestamp_col_li = getattr(map_schema, datetime_cols_param)

# Initialize the API reader, process data, and write to Redshift
api_reader = ReadAPI(appname, table_schema, timestamp_col_li)
df = api_reader.execute()
input_dynamic_frame = DynamicFrame.fromDF(df, glueContext, "input_dynamic_frame")
write_to_redshift(glueContext, input_dynamic_frame)
