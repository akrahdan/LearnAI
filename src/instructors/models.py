from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.

class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120, null=True, blank=True)
    last_name = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self) -> str:
       return self.user.username
        