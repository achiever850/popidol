
database = ""

class CallExternalIdApi():
    def __init__(self, api_url):
        self.api_url = api_url

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
    
    def write_to_redshift(self, df, table_name):
        my_conn_options = {
            "dbtable": table_name,
            "database": database
            }
        print(f"Writing into redshift table: {my_conn_options}")
        input_dynamic_frame = DynamicFrame.fromDF(df, glueContext, "input_dynamic_frame")
        glueContext.write_dynamic_frame.from_jdbc_conf(
            frame = input_dynamic_frame, 
            catalog_connection = "dc-connection-name", 
            connection_options = my_conn_options, 
            redshift_tmp_dir = "")
        print(f"Loaded for - {table_name}")
    
    def handle_raw_dict(self,raw_dict):
        for key in raw_dict:
            print(f":::::::::: converting to df and appending for {key} ::::::::::::")
            api_raw_list = raw_dict[key]
            df = self.convert_raw_list_to_df(api_raw_list)
            # for each df append to the respective table.
            table_name = key.lower().Replace('ids','id')
            self.write_to_redshift(df, table_name)

    def execute(self):
        raw_dict = self.fetch_api_data(self.api_url)
        self.handle_raw_dict(raw_dict)
        
        
res=[(32,),(12,),(121,)]
tenantId = '8'
external_base_url = "https://developer.usastaffing.gov/api/offices/{uniqueKey}/externalids"
for rec in res:
    ext_id = rec[0]
    formed_unique_id = f"{tenantId}|{ext_id}"
    uniq_ext_url = external_base_url.replace('{uniqueKey}',formed_unique_id)
    print(uniq_ext_url)
    pointer = CallExternalIdApi(uniq_ext_url)
    pointer.execute()
    
