# Import the SDK
import boto3
import argparse
import re

# Argparser definition
parser = argparse.ArgumentParser(
    description='Command to count the number of files within a bucket in AWS')
parser.add_argument('-b', '--bucket-name', help='Bucket name', required=True)
parser.add_argument('-p', '--prefix', help='Prefix for files', required=False)
args = parser.parse_args()

s3resource = boto3.resource('s3')

bucket = s3resource.Bucket(args.bucket_name)
p = None

if args.prefix:
    p = re.compile(ur'^%s(.*)' % args.prefix)

total = 0
total_prefix = 0

for key in bucket.objects.all():
    if args.prefix and re.search(p, key.key):
        total_prefix += 1

    total += 1

if args.prefix:
    print u'There are a total of %s object(s) with prefix %s out of %s in %s bucket' % (
    total_prefix, args.prefix, total, args.bucket_name)
else:
    print u'There are a total of %s object(s) in %s bucket' % (total, args.bucket_name)
