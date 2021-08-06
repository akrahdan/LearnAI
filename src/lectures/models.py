from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import related
from django.utils import timezone
from django.db.models.signals import pre_save
from courses.models import Course
from django.conf import settings
import datetime
import vimeo
from ordered_model.models import OrderedModel, OrderedModelManager
from files.models import CourseFile
from readux.db.models import PublishStateOptions
from readux.db.receivers import publish_state_pre_save, slugify_pre_save, unique_slugify_pre_save
from readux.db.utils import generate_lecture_id
from instructors.models import Instructor
# Create your models here.

from django.conf import settings

User = settings.AUTH_USER_MODEL


class LectureQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.LIVE,
            publish_timestamp_lte=now
        )


class LectureManager(OrderedModelManager):
    def published(self):
        return self.get_queryset().published()


class SectionManager(OrderedModelManager):
    pass


class Section(OrderedModel):
    title = models.CharField(max_length=120)
    instructor = models.ForeignKey(
        Instructor, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    course = models.ForeignKey(
        Course, related_name="sections", on_delete=models.CASCADE)
    neighbor = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL)
    position = models.CharField(max_length=20, null=True, blank=True)
    objects = SectionManager()

    def is_fully_filled(self):
        field_names = [self.title,
                       self.course,  self.instructor]
        if any(field is None or field == '' for field in field_names) is True:
            return False
        else:
            return True

    class Meta(OrderedModel.Meta):
        pass

    def __str__(self) -> str:

        return self.title


class Lecture(OrderedModel):
    title = models.CharField(max_length=220)
    instructor = models.ForeignKey(
        Instructor, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True, null=True)
    section = models.ForeignKey(
        Section, related_name='lectures', blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=220, blank=True, null=True)
    lecture_id = models.CharField(max_length=220, unique=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True)
    state = models.CharField(
        max_length=8, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(
        auto_now_add=False, auto_now=False, blank=True, null=True)
    video_url = models.CharField(max_length=300, blank=True, null=True)
    video = models.ForeignKey(CourseFile, null=True,  blank=True,
                              related_name='lecture', on_delete=models.SET_NULL)
    resources = models.ManyToManyField(
        CourseFile, related_name="lectures", blank=True)
    filename = models.CharField(max_length=300, blank=True, null=True)
    neighbor = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.SET_NULL)
    position = models.CharField(max_length=20, null=True, blank=True)

    def is_fully_filled(self):
        field_names = [self.title,
                          self.video_url,  self.instructor, self.video, self.section]
        if any(field is None or field == '' for field in field_names) is True:
            return False
        else:
            return True

    class Meta(OrderedModel.Meta):
        pass

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
            token=settings.VIMEO_ACCESS_TOKEN,
            key=settings.VIMEO_CLIENT_ID,
            secret=settings.VIMEO_SECRET_KEY
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
