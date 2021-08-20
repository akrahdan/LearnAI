from django.db import models
from django.db.models.signals import pre_save
from taggit.managers import TaggableManager
from courses.models import Course
from instructors.models import Instructor
from readux.db.models import PublishStateOptions
from ordered_model.models import OrderedModel, OrderedModelManager
from readux.db.receivers import unique_slugify_pre_save
from project_categories.models import ProjectCategory
# Create your models here.


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    occupation = models.CharField(max_length=120)
    quote = models.TextField()
 
class ProjectSection(models.Model):
    heading = models.CharField(max_length=120)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.heading




class Project(models.Model):
    class ProjectLevelOptions(models.TextChoices):
       BEGINNER = ('Beginner', 'Beginner')
       INTERMEDIATE = ('intermediate', 'Intermediate')
       ADVANCED = ('advanced', 'Advanced')
       DEEP = ('deep', 'Deep Dive')
       

    title = models.CharField(max_length=120)
    lead = models.BooleanField(default=False)
    description = models.TextField()
    slug = models.SlugField(max_length=200, blank=True, null=True)
    goal = models.CharField(max_length=120, blank=True, null=True)
    hero = models.CharField(max_length=120, blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, null=True)
    category = models.ForeignKey(ProjectCategory, blank=True, null=True, on_delete=models.SET_NULL)
    instructor = models.ForeignKey(Instructor, related_name="projects", on_delete=models.CASCADE)
    experience = models.CharField(max_length=12, choices=ProjectLevelOptions.choices, default=ProjectLevelOptions.BEGINNER)
    courses = models.ManyToManyField(Course, related_name='projects', blank=True)
    completion_time = models.CharField(max_length=120, blank=True, null=True)
    related = models.ManyToManyField("self", blank=True, related_name="related", through="ProjectRelated")
    header = models.ForeignKey(ProjectSection, related_name='projects', blank=True, null=True, on_delete=models.SET_NULL)
    header_primary_color= models.CharField(max_length=100, blank=True, null=True)
    header_secondary_color= models.CharField(max_length=100, blank=True, null=True)
    testimonial = models.ForeignKey(Testimonial, blank=True, null=True, on_delete=models.SET_NULL)
    video_headline = models.CharField(max_length=200, blank=True, null=True)
    difficulty = models.CharField(max_length=20, choices=ProjectLevelOptions.choices, default=ProjectLevelOptions.BEGINNER)
    progress = models.DecimalField(max_length=100, default=0.0, null=True, blank=True, decimal_places=1, max_digits=3)
    tags = TaggableManager(blank=True)
    updated = models.DateTimeField(auto_now=True)
    price  = models.DecimalField(decimal_places=2, max_digits=20, default=39.99,  blank=True, null=True)
    state = models.CharField(max_length=20, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
       

   
 
class ProjectRelatedManager(OrderedModelManager):
    pass

class ProjectRelated(OrderedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    related = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='related_item')
    
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProjectRelatedManager()

    class Meta(OrderedModel.Meta):
        pass


class SyllabusManager(OrderedModelManager):
    pass

class LearningOutcomeManager(OrderedModelManager):
    pass



class TitleDescriptionManager(OrderedModelManager):
    pass

class Syllabus(OrderedModel):
    title = models.CharField(max_length=120)
    project = models.ForeignKey(Project, related_name="syllabuses", on_delete=models.CASCADE)
    description = models.TextField()
    instructor = models.ForeignKey(Instructor, blank=True, null=True, on_delete=models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = SyllabusManager()

    def __str__(self) -> str:
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class LearningOutCome(OrderedModel):
    title = models.CharField(max_length=120)
    instructor = models.ForeignKey(Instructor, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, related_name='outcomes', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = LearningOutcomeManager()

    def __str__(self) -> str:
        return self.title

    class Meta(OrderedModel.Meta):
        pass


class TitleDescription(OrderedModel):
    title = models.CharField(max_length=120)
    instructor = models.ForeignKey(Instructor, blank=True, null=True, on_delete=models.SET_NULL)
    project = models.ForeignKey(Project, related_name="included", on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TitleDescriptionManager()

    def __str__(self) -> str:
        return self.title

    class Meta(OrderedModel.Meta):
        pass


pre_save.connect(unique_slugify_pre_save, sender=Project)