# AWS scripts
These are some useful scripts to work with AWS.

In order to execute any of this scripts, you must install [boto3][1] 
and you must set up [your authentication credentials][2].

[1]: http://boto3.readthedocs.io/en/latest/guide/quickstart.html#installation
[2]: http://boto3.readthedocs.io/en/latest/guide/quickstart.html#configuration

List of scripts:
- [Count objects within a bucket](#count-objects-within-a-bucket)
- [Update Content-Type of all objects within a bucket](#update-content-type-of-all-objects-within-a-bucket)

===
## Count objects within a bucket

The script `count-objects.py` counts the total objects within a bucket.
Optionally, a prefix may be passed in order to count the total objects
that starts with that prefix.

Usage:

```bash
$ python count-objects.py -h

usage: count-objects.py [-h] -b BUCKET_NAME [-p PREFIX]

Command to count the number of files within a bucket in AWS

optional arguments:
  -h, --help            show this help message and exit
  -b BUCKET_NAME, --bucket-name BUCKET_NAME
                        Bucket name
  -p PREFIX, --prefix PREFIX
                        Prefix for files
```

Examples of usage.

### Count all objects within a bucket

```bash
$ python count-objects.py -b bucket_name
```

Output:

```bash
There are a total of 3099 object(s) in bucket_name bucket
```

### Count all objects within a bucket with a prefix

```bash
$ python count-objects.py -b bucket_name -p xxxx
```

Output:

```bash
There are a total of 10 object(s) with prefix xxxx out of 3099 in bucket_name bucket
```

===
## Update Content-Type of all objects within a bucket

The script `update-content-type.py` updates the Content-Type of all
objects within a bucket. Optionally, it creates a backup of the
original object.

The workflow for changing the content-type of an existing object is:

1. Backup the object creating a new one with another name and applying the metadata and permissions required
2. Remove the original object
3. Restore the backed up object into the original one, applying the metadata and permissions required
4. (Optional) Remove the backup file

Usage:

```bash
$ python update-content-type.py -h
usage: update-content-type.py [-h] -b BUCKET_NAME -c CONTENT_TYPE -p
                              BACKUP_PREFIX [--backup]

Command to change the Content-Type of files within a bucket of AWS

optional arguments:
  -h, --help            show this help message and exit
  -b BUCKET_NAME, --bucket-name BUCKET_NAME
                        Bucket name
  -c CONTENT_TYPE, --content-type CONTENT_TYPE
                        Content-Type to set files to
  -p BACKUP_PREFIX, --backup-prefix BACKUP_PREFIX
                        Prefix for backups
  --backup              Whether to preserve the backups created
```

Examples of usage.

### Change Content-Type to be audio/mpeg without backup

```bash
$ python update-metadata.py -b bucket_name -p xxxx -c audio/mpeg
```

Output:

```bash
A total of 3099 objects within bucket bucket_name have been updated
```

### Change Content-Type to be audio/mpeg with backup

```bash
$ python update-metadata.py -b bucket_name -p xxxx -c audio/mpeg --backup
```

Output:

```bash
A total of 3099 objects within bucket bucket_name have been updated
```