import boto3
import gzip
import re 

txt_prefix = 'gz_files'
gz_directory = 'gz_files/'
txt_directory = 'txt_files/'

def get_ip(content):
    print('content', content)
    pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
    ip_addresses = re.findall(pattern, content)
    return ip_addresses



ips = []
s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2'
)

gz_files = []
for obj in s3.Bucket('i-morgen-logs').objects.all():
    s3.Bucket('i-morgen-logs').download_file(Key=obj.key, Filename=gz_directory + obj.key)
    gz_files.append(obj.key)

for gz_file in gz_files:
    with gzip.open(gz_directory + gz_file, 'rb') as f:
        contents = f.read()
    ips.append(get_ip(contents.decode('utf-8')))
    txt_file = txt_prefix + gz_file.replace('.gz', '.txt')
    with open(txt_directory + txt_file, 'wb') as f:
        f.write(contents)

with open(txt_directory + "ip_addresses.txt", 'wb') as f:
    flat_ip = flat_list = [item for sublist in ips for item in sublist]
    f.write(str((flat_ip)).encode('utf-8'))

# print(ips)