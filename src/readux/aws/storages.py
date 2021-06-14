from storages.backends.s3boto3 import S3Boto3Storage

StaticS3Storage = lambda: S3Boto3Storage(location='static')
MediaS3Storage = lambda: S3Boto3Storage(location='media')