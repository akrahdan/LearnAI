from django.db import models
from django.conf import settings
# Create your models here.
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .signals import object_viewed_signal
from lectures.models import Lecture
User = settings.AUTH_USER_MODEL

class ObjectViewed(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    

    def __str__(self) -> str:
        return f"{self.content_object} viewed on {self.timestamp}"
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'

class LectureProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE)
    thumbnail = models.URLField(blank=True, null=True)
    progress = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.lecture.title



def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender) # instance.__class__
    user = None
    if request.user.is_authenticated:
        user = request.user
    new_view_obj = ObjectViewed.objects.create(
                user = user,
                content_type=c_type,
                object_id=instance.id,
                
        )


object_viewed_signal.connect(object_viewed_receiver)


