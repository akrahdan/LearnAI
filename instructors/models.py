from django.db import models
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField
from taggit.managers import TaggableManager
User = settings.AUTH_USER_MODEL

# Create your models here.

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    avatar = models.URLField(max_length=220, null=True, blank=True)
    headline = models.CharField(max_length=220, blank=True, null=True)
    email = models.EmailField(max_length=120, blank=True, null=True)
    phone = PhoneNumberField()
    view = models.BooleanField(default=True)
    tags = TaggableManager()
    
    @property
    def get_fullname(self):
      name = f"{self.first_name}  {self.last_name}"
      return name
   


    def __str__(self) -> str:
       return self.user.username
        