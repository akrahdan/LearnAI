from django.db import models
import os
from django.conf import settings
from django.utils.text import slugify
from readux.aws.utils import AWS
from courses.models import Course
from projects.models import Project
User = settings.AUTH_USER_MODEL

def user_directory_path(instance, filename):
    # file will be uploaded to bucket/user_<id>/<filename>
    return 's3files/user_{0}/{1}'.format(instance.user.id, filename)


class S3File(models.Model):
    user        = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    name        = models.CharField(max_length=220, blank=True, null=True)
    key         = models.TextField() # key path in aws "path"
    filetype    = models.CharField(max_length=120, default='video/mp4')
    uploaded    = models.BooleanField(default=False) # true / false
    active      = models.BooleanField(default=True)  # show in resuls
    size        = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True) # size of file
    duration    = models.DecimalField(max_digits=30, decimal_places=6, blank=True, null=True)
    updated     = models.DateTimeField(auto_now=True)# any changes
    timestamp   = models.DateTimeField(auto_now_add=True)# when added
    
    def get_file_ext(self):
        return os.path.splitext(self.key)[1] # path/to/file/upload.png - > path/to/file/upload, .png

    def get_filename(self):
        custom = self.name
        if custom:
            ext = self.get_file_ext() # .png
            if custom.endswith(ext):
                custom, ext = os.path.splitext(custom) # this is-my-file.png
            custom = slugify(custom)
            custom = f'{custom}{ext}' # this-is-my-file.png
            return custom
        return os.path.basename(self.key) 

    def get_download_url(self):
        key = self.key
        name = self.get_filename()
        botoReadux = AWS()
        return botoReadux.get_download_url(key=key, force_download=False, filename=name) #, expires_in=10)


class CourseFile(models.Model):
    course      = models.ForeignKey(Course, null=True, related_name='files', on_delete=models.SET_NULL)
    name        = models.CharField(max_length=220, blank=True, null=True)
    key         = models.TextField() # key path in aws "path"
    filetype    = models.CharField(max_length=120, default='video/mp4')
    uploaded    = models.BooleanField(default=False) # true / false
    active      = models.BooleanField(default=True)  # show in resuls
    size        = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True) # size of file
    duration    = models.DecimalField(max_digits=30, decimal_places=6, blank=True, null=True)
    updated     = models.DateTimeField(auto_now=True)# any changes
    timestamp   = models.DateTimeField(auto_now_add=True)# when added
    
    def __str__(self) -> str:
        return self.name
    def get_file_ext(self):
        return os.path.splitext(self.key)[1] # path/to/file/upload.png - > path/to/file/upload, .png

    def get_filename(self):
        custom = self.name
        if custom:
            ext = self.get_file_ext() # .png
            if custom.endswith(ext):
                custom, ext = os.path.splitext(custom) # this is-my-file.png
            custom = slugify(custom)
            custom = f'{custom}{ext}' # this-is-my-file.png
            return custom
        return os.path.basename(self.key) 

    def get_download_url(self):
        key = self.key
        name = self.get_filename()
        botoReadux = AWS()
        return botoReadux.get_download_url(key=key, force_download=False, filename=name) #, expires_in=10)




class ProjectFile(models.Model):
    project      = models.ForeignKey(Project, null=True, related_name='files', on_delete=models.SET_NULL)
    name        = models.CharField(max_length=220, blank=True, null=True)
    key         = models.TextField() # key path in aws "path"
    filetype    = models.CharField(max_length=120, default='video/mp4')
    uploaded    = models.BooleanField(default=False) # true / false
    active      = models.BooleanField(default=True)  # show in resuls
    size        = models.DecimalField(max_digits=30, decimal_places=4, blank=True, null=True) # size of file
    duration    = models.DecimalField(max_digits=30, decimal_places=6, blank=True, null=True)
    updated     = models.DateTimeField(auto_now=True)# any changes
    timestamp   = models.DateTimeField(auto_now_add=True)# when added
    
    def get_file_ext(self):
        return os.path.splitext(self.key)[1] # path/to/file/upload.png - > path/to/file/upload, .png

    def get_filename(self):
        custom = self.name
        if custom:
            ext = self.get_file_ext() # .png
            if custom.endswith(ext):
                custom, ext = os.path.splitext(custom) # this is-my-file.png
            custom = slugify(custom)
            custom = f'{custom}{ext}' # this-is-my-file.png
            return custom
        return os.path.basename(self.key) 

    def get_download_url(self):
        key = self.key
        name = self.get_filename()
        botoReadux = AWS()
        return botoReadux.get_download_url(key=key, force_download=False, filename=name) #, expires_in=10)









