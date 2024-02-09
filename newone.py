
import requests
from awsglue.dynamicframe import DynamicFrame
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, LongType, DoubleType, BooleanType
from pyspark.sql.functions import to_timestamp, regexp_replace, when ,concat, col, lit, udf

spark = SparkSession.builder.appName("api-to-df").getOrCreate()
from pyspark.sql.functions import col, to_timestamp

glueContext=sc

base_api_url = ""
api_key = ""
headers={"Api-Key":api_key}

batch_size=100

my_conn_options = {
    "dbtable": "redshift-table-name",
    "database": "redshift-database-name"
    }

@udf(returnType=StringType())
def extract_id_from_links(links, rel_value):
    for link in links:
        if link['rel'] == rel_value:
            try:
                if('/by/' in link['href'].casefold()):
                    val = link['href'].split('/')[-1]
                    res = val.split('|')[-1]
                    return res
                else:
                    val = link['href'].split('/')[4]
                    res = val.split('|')[-1]
                    return res
            except Exception as e:
                print(link['href'])
                print(e)
    return None

class ReadAPI:
    def __init__(self, table_name, api_url_key, table_schema, timestamp_col_li):
        self.headers = headers
        self.table_schema = table_schema
        self.timestamp_columns = timestamp_col_li
        self.api_url = base_api_url+"/api/"+api_url_key
        self.table_name = table_name
        

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
    
    def handle_links(self):
        df = self.df
        print("::: the rel list :::")
        print(self.links_rel_list)
        for rel_value in self.links_rel_list:
            print(f"Extracting for : {rel_value}")
            df = df.withColumn(rel_value, lit(extract_id_from_links(col("_links"), lit(rel_value))))
        print("converting json to text object")
        # df = df.withColumn('_links',col('_links').cast(StringType()))
        df = df.drop('_links')
        self.df = df

    def handle_timestamp_columns(self):
        for column in self.timestamp_columns:
            self.df = self.df.withColumn(column, when(~col(column).contains('.'), concat(col(column), lit('.000'))).otherwise(col(column)))
            self.df = self.df.withColumn(column, to_timestamp(col(column), "yyyy-MM-dd'T'HH:mm:ss.SSSSSSSSS"))

    def write_to_redshift(self):
        self.handle_links()
        self.handle_timestamp_columns()
        print(f"Writing into redshift table: {my_conn_options}")
        input_dynamic_frame = DynamicFrame.fromDF(self.df, glueContext, "input_dynamic_frame")
        glueContext.write_dynamic_frame.from_jdbc_conf(
            frame = input_dynamic_frame, 
            catalog_connection = "dc-connection-name", 
            connection_options = my_conn_options, 
            redshift_tmp_dir = "")
        print(f"Loaded till - {self.currentpage}")

    def process_next_df(self):
        raw_api_data = self.fetch_api_data(base_api_url+self.next_api_url)
        if (raw_api_data):
            self.handle_pagination(raw_api_data)
            raw_api_data_list = raw_api_data['data']
            new_df = self.convert_raw_list_to_df(raw_api_data_list)
            self.concat_df(new_df)

    def mark_checkpoint(self):
        print("----------------------------------------------------------------------")
        print(f"---------------------PageNo: {self.currentpage} pages processed -------------------------")
        print("----------------------------------------------------------------------")
        print("emptying the df")
        self.df = spark.createDataFrame([],schema=self.table_schema)
    
    def mark_begining(self):
        print("=============================================================================")
        print(f"""=========================== {self.table_name} =========================================
            totalCount = {self.totalcount}
            pageSize = {self.pagesize}
            totalPages = {self.totalpages}
            snapshot = {self.snapshot}""")
        print("=============================================================================")

    def execute(self):
        # first time operation
        raw_api_data = self.fetch_api_data(self.api_url)
        self.extract_links_rel_list(raw_api_data)
        if (raw_api_data):
            self.handle_pagination(raw_api_data)
            raw_api_data_list = raw_api_data['data']
            self.df = self.convert_raw_list_to_df(raw_api_data_list)
            for i in range(2,self.totalpages+1):
                if (i%batch_size==0):
                    # append the data in the redsfhit
                    self.write_to_redshift()
                    # empty the df 
                    self.df = self.df.filter("1=0")
                    self.mark_checkpoint()
                    # begin again
                    self.process_next_df()
                elif (i==self.totalpages+1):
                    self.process_next_df()
                    self.write_to_redshift()
                else:
                    self.process_next_df()
        print("Completed the process.")

import map_schema as mp

table_dict = {
    1:"Announcement",
    2:"Application",
    3:"Assessment",
    4:"CertificateApplication",
    5:"Certificate",
    6:"Customer",
    7:"NewHireAppointingAuthority",
    8:"Office",
    9:"OnboardingTask",
    10:"Organization",
    11:"RequestAppointingAuthority",
    12:"Request",
    13:"Review",
    14:"StaffingTask",
    15:"TimeToHire",
    16:"VacancyAppointingAuthority",
    17:"VacancyFlag",
    18:"Vacancy"}

process_tables = []

for i in process_tables:
    table_name = table_dict[i]
    table_schema, timestamp_col_li, api_url_key = mp.get_table_attributes(table_name)
    api_reader = ReadAPI(table_name, api_url_key, table_schema, timestamp_col_li)
    df = api_reader.execute()
