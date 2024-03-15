import aiohttp
import asyncio
from time import perf_counter
import json
import pandas as pd
import os 
import time

# Define a function to call the API and process response
table_name = "prakash_csv_test.office"
folder_path = f"C:/Users/VHALASTeratB/Desktop/codespace/Threesteps/outputs//{table_name.split('.')[-1]}_dir"
external_base_url = "https://developer.usastaffing.gov/api/offices/{uniqueKey}/externalids"

rejection_file = f"{folder_path}/{table_name.split('.')[-1]}_rejections.csv"

def append_rejections(data):
    with open(rejection_file, 'a') as f:
        f.writelines(str(data)+"\n")

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder {folder_path} created successfully.")
else:
    print(f"Folder {folder_path} already exists")

json_file_path = "C:/Users/VHALASTeratB/Desktop/codespace/Threesteps/jsons/seventables.json"
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

async def process_url(session, inp):
    url = inp[0]
    num = inp[1]
    try:
        async with session.get(url, headers=headers) as response:
            # Process the response, extract data
            print(num, total_count, url)
            data = await response.json()
            await pandas_process(data)
    except Exception as e:
        print(f"Failed to read api for {url} with error : {e}")
        append_rejections((url,e))

async def main(urls):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[process_url(session, url) for url in urls])





if __name__ == "__main__":
    # List of URLs to process
    urls = []
    tenantId = 8
    total_count = len(ext_data)
    batch_size = 50
    sleep_time = 60
    processid = -1
    print('-----')
    start = perf_counter()
    
    # Loop over the URLs in batches
    for i in range(0, total_count, batch_size):
        batch_urls = []
        for di in ext_data[i:i+batch_size]:
            val = list(di.values())[0]
            if val > processid:
                formed_unique_id = f"{tenantId}|{val}"
                uniq_ext_url = external_base_url.replace('{uniqueKey}', formed_unique_id)
                batch_urls.append((uniq_ext_url, i))
        
        # Process the batch asynchronously
        asyncio.run(main(batch_urls))
        
        # Sleep for 60 seconds
        print(f"Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)
        
    end = perf_counter()
    print(f"Time taken to read : {end - start}")
