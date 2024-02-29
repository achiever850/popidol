import boto3

# Initialize S3 client
s3 = boto3.client('s3')

# Specify the S3 bucket and path
bucket_name = 'your-bucket-name'
folder_path = 'your-folder-path/'

# List objects in the S3 path
response = s3.list_objects_v2(
    Bucket=bucket_name,
    Prefix=folder_path
)

# Extract file names from the response
file_names = [obj['Key'] for obj in response.get('Contents', [])]

# Print the list of file names
for file_name in file_names:
    if file_name.endswith('.csv'):
        print(file_name)
