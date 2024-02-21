def fetch_api_data(api_url):
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code ==200:
            return response.json()
    except Exception as e:
        print(e)
        return  None

def create_struct_schema(data):
    schema_fields=[]
    for k in data[0].keys():
        if k.casefold() != 'tenantid':
            schema_fields.append(StructField(k, LongType(), True))
        else:
            schema_fields.append(StructField(k, IntegerType(), True))
    return (schema_fields)

def extend_lists(dicts_to_merge):
    merged_output = {}
    # dicts_to_merge = [samp_out1, samp_out2, samp_out3]
    for d in dicts_to_merge:
        for key, value in d.items():
            if key not in merged_output:
                merged_output[key] = []
            merged_output[key].extend(value)
    return(merged_output)

def convert_raw_list_to_df(raw_api_data_list, schema):
    df = spark.createDataFrame(raw_api_data_list, schema)
    return df

def create_struct_schema(data):
    schema_fields=[]
    for k in data[0].keys():
        if k.casefold() != 'tenantid':
            schema_fields.append(StructField(k, LongType(), True))
        else:
            schema_fields.append(StructField(k, IntegerType(), True))
    return (schema_fields)

def write_to_redshift(df, table_name):
    my_conn_options = {
        "dbtable": table_name,
        "database": redshift_database
        }
    print(f"Writing into redshift table: {my_conn_options}")
    input_dynamic_frame = DynamicFrame.fromDF(df, glueContext, "input_dynamic_frame")
    glueContext.write_dynamic_frame.from_jdbc_conf(
        frame = input_dynamic_frame, 
        catalog_connection = "dc-connection-name", 
        connection_options = my_conn_options, 
        redshift_tmp_dir = "")
    print(f"Loaded for - {table_name}")

def handle_raw_dict(raw_dict):
    if raw_dict:
        for key, data in raw_dict.items():    
            if data: 
                schema_fields = create_struct_schema(data)
                schema = StructType(schema_fields)
                api_raw_list = raw_dict[key]
                df = convert_raw_list_to_df(api_raw_list, schema)
                # for each df append to the respective table.
                table_name = key.lower().replace('ids','id')
                write_to_redshift(df, table_name)
            

res=[]

tenantId=8
external_base_url = "https://developer.usastaffing.gov/api/offices/{uniqueKey}/externalids"

raw_dict_list=[]
batch_size = 10
for i in range(len(res)):
    rec = res[i]
    ext_id = rec[0]
    formed_unique_id = f"{tenantId}|{ext_id}"
    uniq_ext_url = external_base_url.replace('{uniqueKey}',formed_unique_id)
    print(uniq_ext_url)
    raw_dict = fetch_api_data(uniq_ext_url)
    if raw_dict:
        raw_dict_list.append(raw_dict)
    if(i%batch_size == 0):
        merged_dict = extend_lists(raw_dict_list)
        handle_raw_dict(merged_dict)
        raw_dict_list=[]
    elif (i == len(res)):
        merged_dict = extend_lists(raw_dict_list)
        handle_raw_dict(merged_dict)
