import aiohttp
import asyncio
import csv
import json
import pandas as pd
import os 

# Define a function to call the API and process response
input_file = ""
table_name = "prakash_csv_test.Organization"
folder_path = f"C:/Users/VHALASTeratB/Desktop/Codespace/Threesteps/{table_name.split('.')[-1]}_dir"
external_base_url = "https://developer.usastaffing.gov/api/organizations/{uniqueKey}/externalids"

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder {folder_path} created successfully.")
else:
    print(f"Folder {folder_path} already exists")

json_file_path = "C:/Users/VHALASTeratB/Desktop/Codespace/Threesteps/json/seventables.json"
with open(json_file_path, 'r') as json_file:
    all_tab_ext_data = json.load(json_file)

ext_data = all_tab_ext_data['tables'][table_name]['data']

api_key = "api key here"

headers = {
    'Api-Key':api_key
}

async def append_to_csv(df, key):
    csv_file_path = f"{folder_path}/{key}.csv"
    if not os.path.exists(csv_file_path):
        df.to_csv(csv_file_path, mode='w', header=True, index=False) 
    else:   
        df.to_csv(csv_file_path, mode='a', header=False, index=False)

async def pandas_process(data):
    tasks = [append_to_csv(pd.DataFrame(data[key]), key) for key in data]
    await asyncio.gather(*tasks)

async def process_url(session, url):
    try:
        async with session.get(url, headers=headers) as response:
            # Process the response, extract data
            data = await response.json()
            await pandas_process(data)
    except Exception as e:
        print(e)

async def main(urls):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[process_url(session, url) for url in urls])

# List of URLs to process
urls = []
tenantId = 8


for di in ext_data:
    val = list(di.values())[0]
    formed_unique_id = f"{tenantId}|{val}"
    uniq_ext_url = external_base_url.replace('{uniqueKey}', formed_unique_id)
    urls.append(uniq_ext_url)

# Run the main coroutine with asyncio
asyncio.run(main(urls))
