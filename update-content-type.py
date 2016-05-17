# -*- coding: utf-8 -*-

import argparse
import re

# Import the SDK
import boto3

"""
The workflow for changing the content-type of an existing object is:
    1. Backup the object creating a new one with another name and applying the metadata and permissions required
    2. Remove the original object
    3. Restore the backed up object into the original one, applying the metadata and permissions required
    4. (Optional) Remove the backup file
"""

# Argparser definition
parser = argparse.ArgumentParser(
    description='Command to change the Content-Type of files within a bucket of AWS')
parser.add_argument('-b', '--bucket-name', help='Bucket name', required=True)
parser.add_argument('-c', '--content-type', help='Content-Type to set files to', required=True)
parser.add_argument('-p', '--backup-prefix', help='Prefix for backups', required=True)
parser.add_argument('--backup', help='Whether to preserve the backups created', dest='preserve_backup',
                    action='store_true')
parser.set_defaults(preserve_backup=False)
args = parser.parse_args()

bucket_name = args.bucket_name

# Create 
s3client = boto3.client('s3')
s3resource = boto3.resource('s3')

# Set required variables
bucket = s3resource.Bucket(bucket_name)
prefix = args.backup_prefix
p = re.compile(ur'^%s(.*)' % prefix)

total = 0

for key in bucket.objects.all():
    # Set file names
    original_key = key.key
    backup_key = u'%s%s' % (prefix, original_key)

    # Prevent doing backups of backups, as *all* method reloads all information from bucket
    if re.search(p, original_key):
        continue

    # Set object sources
    original_key_source = u'%s/%s' % (bucket_name, original_key)
    backup_key_source = u'%s/%s' % (bucket_name, backup_key)

    # 1. Copy the original object into a new one, changing permissions and content-type
    s3client.copy_object(Bucket=bucket_name, CopySource=original_key_source, Key=backup_key,
                         ContentType=args.content_type, MetadataDirective='REPLACE', ACL='public-read')

    # 2. Remove the original object
    s3client.delete_object(Bucket=bucket_name, Key=original_key)

    # 3. Restore the backed up object into the original one
    s3client.copy_object(Bucket=bucket_name, CopySource=backup_key_source, Key=original_key,
                         ContentType=args.content_type, MetadataDirective='REPLACE', ACL='public-read')

    # 4. Remove backup object, if required
    if not args.preserve_backup:
        s3client.delete_object(Bucket=bucket_name, Key=backup_key)

    total += 1

print u'A total of %s objects within bucket %s have been updated' % (str(total), bucket_name)
exit(0)
