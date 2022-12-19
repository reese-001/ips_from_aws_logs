import boto3
import gzip

# Create an S3 client
s3 = boto3.client('s3')

# Set the name of the S3 bucket and the prefix for the .gz files
bucket_name = 'i-morgen-logs'
prefix = '/'

# Use the S3 client to list all of the .gz files in the bucket with the specified prefix
objects = s3.list_objects(Bucket=bucket_name, Prefix=prefix)
gz_files = [obj['Key'] for obj in objects['Contents']]

# Iterate through the list of .gz files
for gz_file in gz_files:
    # Download the .gz file
    print(f'Downloading {gz_file}...')
    s3.download_file(bucket_name, gz_file, gz_file)
    # Open the .gz file for reading
    with gzip.open(gz_file, 'rb') as f:
        # Read the contents of the .gz file
        contents = f.read()
    # Write the contents to a .txt file with the same name as the .gz file
    txt_file = gz_file.replace('.gz', '.txt')
    with open(txt_file, 'wb') as f:
        f.write(contents)
