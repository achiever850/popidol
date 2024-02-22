import concurrent.futures
import requests
import csv

# Define a function to call the API and process response
def process_url(url):
    response = requests.get(url)
    # Process the response, extract data
    data = response.json()
    # Write data to CSV
    with open('output.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)


# List of URLs to process
urls = [...]

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
