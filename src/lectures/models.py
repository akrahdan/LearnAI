from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.utils import timezone
from django.db.models.signals import pre_save
from courses.models import Course
from django.conf import settings
import datetime
import vimeo
from readux.db.models import PublishStateOptions
from readux.db.receivers import publish_state_pre_save, slugify_pre_save, unique_slugify_pre_save
from readux.db.utils import generate_lecture_id
# Create your models here.

from django.conf import settings

User = settings.AUTH_USER_MODEL
    
class LectureQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.LIVE,
            publish_timestamp_lte = now
        )

class LectureManager(models.Manager):
    def get_queryset(self):
        return LectureQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()

class Section(models.Model):
    title = models.CharField(max_length=120)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    course = models.ForeignKey(Course, related_name="sections", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title
    
class Lecture(models.Model):
    title = models.CharField(max_length=220)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    section = models.ForeignKey(Section, related_name='lectures', blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=220, blank=True, null=True)
    lecture_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=4, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    video_url = models.CharField(max_length=300, blank=True, null=True)
    filename = models.CharField(max_length=300, blank=True, null=True)

    
    objects = LectureManager()

    def __str__(self) -> str:
        return self.title

    def get_lecture_id(self):
        if not self.is_published:
            return None
        return self.lecture_id
    
    def get_duration(self):
        vimeo_data = self.vimeo_data()
        seconds = vimeo_data["duration"]
        converted_time = datetime.timedelta(seconds=seconds)
        return converted_time
    
    def vimeo_data(self):
        v = vimeo.VimeoClient(
            token= settings.VIMEO_ACCESS_TOKEN,
            key= settings.VIMEO_CLIENT_ID,
            secret= settings.VIMEO_SECRET_KEY
        )
        
        video_url = self.video_url
        if video_url is None:
            return

        data = v.get(video_url, jsonify=True).json()
        return data

    def get_vimeo_url(self):
        vimeo_data = self.vimeo_data()
        return vimeo_data.get("embed")
    
   




    @property
    def is_published(self):
        if self.active is False:
            return False
        state = self.state
        if state != PublishStateOptions.LIVE:
            return False
        pub_timestamp = self.publish_timestamp
        if pub_timestamp is None:
            return False
        now = timezone.now()
        return pub_timestamp <= now

def pre_save_create_lecture_id(sender, instance, *args, **kwargs):
    if not instance.lecture_id:
        instance.lecture_id = generate_lecture_id(instance)

    



class LecturePublishedProxy(Lecture):
    class Meta:
        proxy = True
        verbose_name = "Published Lecture"
        verbose_name_plural = "Published Lectures"



pre_save.connect(publish_state_pre_save, sender=Lecture)
pre_save.connect(unique_slugify_pre_save, sender=Lecture)
pre_save.connect(pre_save_create_lecture_id, sender=Lecture)
