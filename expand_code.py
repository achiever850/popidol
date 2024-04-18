import aiohttp
import asyncio
from time import perf_counter
import json
import pandas as pd
import os 
import time
import requests
# Define a function to call the API and process response
table_name = "staffingtask"
key_value = "staffingTaskExternalIDs"
folder_path = f"C:/Users/VHALASTeratB/Desktop/codespace/Threesteps/outputs/{table_name.split('.')[-1]}_dir"

base_url = "https://developer.usastaffing.gov"
main_ext_url = f"https://developer.usastaffing.gov/api/{table_name}s?expand={table_name}externalids"

rejection_file = f"{folder_path}/{table_name.split('.')[-1]}_rejections.csv"

def append_rejections(data):
    with open(rejection_file, 'a') as f:
        f.writelines(str(data)+"\n")

if not os.path.exists(folder_path):
    os.makedirs(folder_path)
    print(f"Folder {folder_path} created successfully.")
else:
    print(f"Folder {folder_path} already exists")

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

async def pandas_process(raw_data,key_value):
    all_data=raw_data['data']
    tasks = [[append_to_csv(pd.DataFrame(data[key]), key) for key in data[key_value]] for data in all_data]
    await asyncio.gather(*tasks)

async def process_url(session, inp):
    url = inp[0]
    num = inp[1]
    try:
        async with session.get(url, headers=headers) as response:
            # Process the response, extract data
            print(num, total_pages, url)
            data = await response.json()
            await pandas_process(data)
    except Exception as e:
        print(f"Failed to read api for {url} with error : {e}")
        append_rejections((url,e))

async def main(urls):
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[process_url(session, url) for url in urls])


def handle_pagination(raw_api_data):
    page_dict = raw_api_data['paging']
    metadata = {
    "totalcount" : page_dict['metadata']['totalCount'],
    "pagesize" : page_dict['metadata']['pageSize'],
    "currentpage" : page_dict['metadata']['currentPage'],
    "totalpages" : page_dict['metadata']['totalPages'],
    "snapshot" : page_dict['metadata']['snapshot'],
    "previous" : page_dict['previous'],
    "next_api_url" : page_dict['next']}
    return metadata

def run_first():
    response = requests.get(main_ext_url)
    # Process the response, extract data
    if response.status_code == 200:
        data = response.json()
        metadata = handle_pagination(data)
    else:
        raise Exception(f"failed to read data at from url : {main_ext_url}")
    return metadata

def handle_pagenum(next_api_url):
    # next_api_url = "/api/NewHires?expand=NewHireexternalIDs&pagesize=1000&pagenumber=2&snapshot=SS7"
    and_li = next_api_url.split("&")
    new_and_li=[]
    for val in and_li:
        if ('pagenumber' in val):
            new_and_li.append("pagenumber={pp_num}")
        else:
            new_and_li.append(val)
    return "&".join(new_and_li)


if __name__ == "__main__":
    # List of URLs to process
    metadata = run_first()
    urls = []
    tenantId = 8
    total_pages = metadata["totalpages"]
    next_ff_url = handle_pagenum(metadata["next_api_url"])

    batch_size = 50
    sleep_time = 60
    processPage = -1
    print('-----')
    start = perf_counter()
    
    # Loop over the URLs in batches
skip = False
for i in range(1, total_pages+1, batch_size):
    batch_urls = []
    for j in range(i,i+batch_size):
        page_num = j
        # print(page_num)
        if page_num > processPage and page_num <= total_pages:
            uniq_ext_url = base_url+next_ff_url.replace('{pp_num}', str(page_num))
            batch_urls.append((uniq_ext_url, j))
            skip = False
        else:
            skip = True
    # print(batch_urls)
        if not skip:
            # Process the batch asynchronously
            asyncio.run(main(batch_urls))
            # Sleep for 60 seconds
            print(f"Sleeping for {sleep_time} seconds...")
            time.sleep(sleep_time)
        
    end = perf_counter()
    print(f"Time taken to read : {end - start}")

