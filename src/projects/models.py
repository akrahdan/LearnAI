from django.db import models
from django.db.models.signals import pre_save
from taggit.managers import TaggableManager
from courses.models import Course
from instructors.models import Instructor
from readux.db.models import PublishStateOptions

from readux.db.receivers import unique_slugify_pre_save
# Create your models here.


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    occupation = models.CharField(max_length=120)
    quote = models.TextField()
 
class ProjectSection(models.Model):
    heading = models.CharField(max_length=120)
    description = models.TextField()




class Project(models.Model):
    class ProjectLevelOptions(models.TextChoices):
       BEGINNER = ('Beginner', 'Beginner')
       INTERMEDIATE = ('intermediate', 'Intermediate')
       ADVANCED = ('advanced', 'Advanced')
       DEEP = ('deep', 'Deep Dive')
       

    title = models.CharField(max_length=120)
    lead = models.BooleanField(default=False)
    description = models.TextField()
    slug = models.SlugField(max_length=200)
    goal = models.CharField(max_length=120)
    hero = models.CharField(max_length=120)
    instructor = models.ManyToManyField(Instructor, related_name="projects")
    experience = models.CharField(max_length=12, choices=ProjectLevelOptions.choices, default=ProjectLevelOptions.BEGINNER)
    courses = models.ManyToManyField(Course, related_name='projects')
    completion_time = models.CharField(max_length=120)
    related = models.ManyToManyField("self", blank=True, related_name="related", through="ProjectRelated")
    header = models.ForeignKey(ProjectSection, blank=True, null=True, on_delete=models.SET_NULL)
    header_primary_color= models.CharField(max_length=100)
    header_secondary_color= models.CharField(max_length=100)
    testimonial = models.ForeignKey(Testimonial, blank=True, null=True, on_delete=models.SET_NULL)
    video_headline = models.CharField(max_length=200)
    difficulty = models.CharField(max_length=20, choices=ProjectLevelOptions.choices, default=ProjectLevelOptions.BEGINNER)
    progress = models.DecimalField(max_length=100, default=0.0, null=True, blank=True, decimal_places=1, max_digits=3)
    tags = TaggableManager(blank=True)
    updated = models.DateTimeField(auto_now=True)
    price  = models.DecimalField(decimal_places=2, max_digits=20, default=39.99,  blank=True, null=True)
    state = models.CharField(max_length=20, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
 
   
class ProjectRelated(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    related = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='related_item')
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

class Syllabus(models.Model):
    title = models.CharField(max_length=120)
    project = models.ForeignKey(Project, related_name="syllabuses", on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

class LearningOutCome(models.Model):
    title = models.CharField(max_length=120)
    project = models.ForeignKey(Project, related_name='outcomes', on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

class TitleDescription(models.Model):
    title = models.CharField(max_length=120)
    project = models.ForeignKey(Project, related_name="included", on_delete=models.CASCADE)
    description = models.TextField()
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

pre_save.connect(unique_slugify_pre_save, sender=Project)