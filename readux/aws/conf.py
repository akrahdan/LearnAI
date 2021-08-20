import datetime
import os

# IAM User
AWS_USER_NAME = 'RDS3User'
AWS_IAM_GROUP = 'RDuce'

AWS_ACCESS_KEY_ID = str(os.environ.get(
        'AWS_ACCESS_ID', 
        'AKIAXKJIYIJVWCCIOXGW'
        ))

AWS_SECRET_ACCESS_KEY = str(os.environ.get(
        'AWS_SECRET_ID', 
        'pbq4su54HddlwdOvyZz0kG0fGkI4rz+2RwlI868p'
        ))

## Django-storages
# Media ROOT # to media/ -> static.growthfromzero.com/media/
DEFAULT_FILE_STORAGE = 'readux.aws.storages.MediaS3Storage'
# Static Root # static/ -> # static.growthfromzero.com/static/
STATICFILES_STORAGE = 'readux.aws.storages.StaticS3Storage'
AWS_STORAGE_BUCKET_NAME = 'cdn.readuced.com'
AWS_DEFAULT_ACL = 'public-read'
AWS_BUCKET_ACL = None
AWS_AUTO_CREATE_BUCKET = False

days_expires = 61
two_months = datetime.timedelta(days=days_expires)
date_two_months_later = datetime.date.today() + two_months
expires = date_two_months_later.strftime("%A, %d %B %Y 20:00:00 GMT")

AWS_HEADERS = {
    'Expires': expires,
    'CacheControl': 'max-age=%d' % (int(two_months.total_seconds()))
}

AWS_S3_OBJECT_PARAMETERS = {
    'Expires': expires,
    'CacheControl': 'max-age=%d' % (int(two_months.total_seconds()))
}

AWS_QUERYSTRING_AUTH = False # sign the url for a static file

AWS_QUERYSTRING_EXPIRE  = 3600
AWS_S3_FILE_OVERWRITE = True
AWS_S3_REGION_NAME = 'us-east-1'

# CDN
#AWS_S3_CUSTOM_DOMAIN = 'cdn.readuced.com'
#AWS_S3_CLOUDFRONT_URL = 'cdn.readuced.com'

# Direct Downloads 
AWS_OBJECT_DOWNLOAD_HOURS = 10


