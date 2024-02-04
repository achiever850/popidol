
import requests
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, LongType, DoubleType, BooleanType
from pyspark.sql.functions import to_timestamp, regexp_replace, when ,concat, col, lit, udf

spark = SparkSession.builder.appName("api-to-df").getOrCreate()
from pyspark.sql.functions import col, to_timestamp



base_api_url = ""
api_key = ""
headers={"Api-Key":api_key}

my_conn_options = {
    "dbtable": "redshift-table-name",
    "database": "redshift-database-name"
    }

@udf(returnType=StringType())
def extract_id_from_links(links, rel_value):
    for link in links:
        if link['rel'] == rel_value:
            try:
                val = link['href'].split('/')[4]
                res = val.split('|')[-1]
                return res
            except Exception as e:
                print(link['href'])
                print(e)
    return None

class ReadAPI:
    def __init__(self, app_name, table_schema, timestamp_col_li):
        self.app_name = app_name
        # self.schema = schema
        self.headers = headers
        self.table_schema = table_schema
        self.timestamp_columns = timestamp_col_li
        self.api_url = base_api_url+"/api/"+app_name
        

    def convert_raw_list_to_df(self, raw_api_data_list):
        df = spark.createDataFrame(raw_api_data_list, schema=self.table_schema)
        return df

    def fetch_api_data(self,api_url):
        try:
            response = requests.get(api_url, headers=self.headers)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(e)
        return None

    def handle_pagination(self, raw_api_data):
        page_dict = raw_api_data['paging']
        self.totalcount = page_dict['metadata']['totalCount']
        self.pagesize = page_dict['metadata']['pageSize']
        self.currentpage = page_dict['metadata']['currentPage']
        self.totalpages = page_dict['metadata']['totalPages']
        self.snapshot = page_dict['metadata']['snapshot']
        self.previous = page_dict['previous']
        self.next_api_url = page_dict['next']

    def extract_links_rel_list(self, raw_api_data):
        link_li = raw_api_data['data'][0]['_links']
        self.links_rel_list = [ele['rel'] for ele in link_li if ele['rel'] != 'self']
        
    def concat_df(self, new_df):
        self.df = self.df.union(new_df)
        print("Concatanating with new df")


    def process_data_for_all_pages(self):
        # while self.next_api_url:
        for i in range(5):
            print(self.next_api_url)
            raw_api_data = self.fetch_api_data(base_api_url+self.next_api_url)
            if (raw_api_data):
                self.handle_pagination(raw_api_data)
                raw_api_data_list = raw_api_data['data']
                new_df = self.convert_raw_list_to_df(raw_api_data_list)
                self.concat_df(new_df)
    
    def handle_links(self):
        df = self.df
        print("::: the rel list :::")
        print(self.links_rel_list)
        for rel_value in self.links_rel_list:
            print(f"Extracting for : {rel_value}")
            df = df.withColumn(rel_value, lit(extract_id_from_links(col("_links"), lit(rel_value))))
        print("converting json to text object")
        df = df.withColumn('_links',col('_links').cast(StringType()))
        self.df = df

    def handle_timestamp_columns(self):
        for column in self.timestamp_columns:
            self.df = self.df.withColumn(column, when(~col(column).contains('.'), concat(col(column), lit('.000'))).otherwise(col(column)))
            self.df = self.df.withColumn(column, to_timestamp(col(column), "yyyy-MM-dd'T'HH:mm:ss.SSSSSSSSS"))

    def execute(self):
        # first time operation
        raw_api_data = self.fetch_api_data(self.api_url)
        if (raw_api_data):
            self.handle_pagination(raw_api_data)
            raw_api_data_list = raw_api_data['data']
            self.df = self.convert_raw_list_to_df(raw_api_data_list)
            if(self.totalpages > 1):
                self.process_data_for_all_pages()

        self.extract_links_rel_list(raw_api_data)
        self.handle_links()
        self.handle_timestamp_columns()
        return self.df


def write_to_redshift(glueContext,input_dynamic_frame):
    glueContext.write_dynamic_frame.from_jdbc_conf(
        frame = input_dynamic_frame, 
        catalog_connection = "dc-connection-name", 
        connection_options = my_conn_options, 
        redshift_tmp_dir = "")
    





appname = ""

import map_schema

table_schema_param = appname+"_schema"
datetime_cols_param = appname+"_timestamp_columns"

table_schema = getattr(map_schema, table_schema_param)
timestamp_col_li = getattr(map_schema, datetime_cols_param)

api_reader = ReadAPI(appname, table_schema, timestamp_col_li)

df = api_reader.execute()

input_dynamic_frame = DynamicFrame.fromDF(df, glueContext, "input_dynamic_frame")
write_to_redshift(glueContext,input_dynamic_frame)



