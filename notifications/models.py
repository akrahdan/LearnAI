from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.
User = settings.AUTH_USER_MODEL
class Notification(models.Model):
    target = models.ForeignKey(User, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='from_user')
    redirect_url = models.URLField(blank=True, null=True, unique=False, max_length=500)
    verb = models.CharField(max_length=255, blank=True, null=True, unique=False)
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    def __str__(self) -> str:
        return self.verb

    def get_content_object_type(self):
        return str(self.content_object.get_cname)