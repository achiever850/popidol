import concurrent.futures
import requests
import csv

output_file="/Users/sathishkumar/AllFiles/vegavega/prop_arch/external_ids/target_file.txt"

# Define a function to call the API and process response
def process_url(url):
    try:
        response = requests.get(url)
        # Process the response, extract data
        data = response.json()
        # Write data to CSV
        with open('output.csv', 'a') as file:
            file.writelines(data)
            # writer = csv.writer(csvfile)
            # writer.writerow(data)
    except Exception as e:
        print(e)




# List of URLs to process
urls = []

tenantId=8
external_base_url = "https://developer.usastaffing.gov/api/offices/{uniqueKey}/externalids"

for i in range(100):
    formed_unique_id = f"{tenantId}|{i}"
    uniq_ext_url = external_base_url.replace('{uniqueKey}',formed_unique_id)
    urls.append(uniq_ext_url)
    
# raw_dict_list=[]
# batch_size = 10
# for i in range(len(res)):
#     rec = res[i]
#     ext_id = rec[0]
#     formed_unique_id = f"{tenantId}|{ext_id}"
#     uniq_ext_url = external_base_url.replace('{uniqueKey}',formed_unique_id)
#     print(uniq_ext_url)
#     raw_dict = fetch_api_data(uniq_ext_url)

# Define the maximum number of threads
MAX_THREADS = 10

# Create a ThreadPoolExecutor
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    # Submit tasks for each URL
    future_to_url = {executor.submit(process_url, url): url for url in urls}
    # Wait for all tasks to complete
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            future.result()
        except Exception as exc:
            print(f"Error processing URL {url}: {exc}")
