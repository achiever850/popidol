batch_size=100

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

appname = ""
appname = appname.lower()
import map_schema

table_schema_param = appname+"_schema"
datetime_cols_param = appname+"_timestamp_columns"

table_schema = getattr(map_schema, table_schema_param)
timestamp_col_li = getattr(map_schema, datetime_cols_param)

api_reader = ReadAPI(appname, table_schema, timestamp_col_li)

df = api_reader.execute()
