from django.contrib import admin

# Register your models here.
from .models import S3File

admin.site.register(S3File)