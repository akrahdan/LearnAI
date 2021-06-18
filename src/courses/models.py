from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils import timezone
from django.db.models import Avg, Max, Min, Q
from django.db.models.signals import pre_save
from taggit.managers import TaggableManager
from readux.db.models import PublishStateOptions
from tags.models import TaggedItem
from ratings.models import Rating
from categories.models import Category
from instructors.models import Instructor
from readux.db.receivers import publish_state_pre_save, slugify_pre_save, unique_slugify_pre_save


COURSE_LEVEL_CHOICES = (
    ('basic', 'Basic'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
    ('deep', 'Deep Dive'),
)
# Create your models here.

class CourseQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            state=PublishStateOptions.LIVE,
            publish_timestamp__lte=now
        )
    
    def search(self, query=None):
        if query is None:
            return self.none()
        return self.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(category__title__icontains=query) |
            Q(tags__tag__icontains=query)
        ).distinct()


class CourseManager(models.Manager):
    def get_queryset(self):
        return CourseQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()

    
    def featured_courses(self):
        return self.get_queryset().filter(level=Course.CourseLevelOptions.FEATURED)

class Course(models.Model):

    class CourseLevelOptions(models.TextChoices):
       BASIC = ('basic', 'Basic')
       INTERMEDIATE = ('intermediate', 'Intermediate')
       ADVANCED = ('advanced', 'Advanced')
       DEEP = ('deep', 'Deep Dive')
       FEATURED = ('featured', "Featured" )
       

    title = models.CharField(max_length=220)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey("self", blank=True, null=True, on_delete=models.SET_NULL)
    instructor = models.ForeignKey(Instructor, null=True, blank=True, related_name='courses', on_delete=models.SET_NULL)
    order = models.IntegerField(default=1, blank=True, null=True)
    level = models.CharField(max_length=120, choices=CourseLevelOptions.choices, default=CourseLevelOptions.BASIC)
    video_url = models.URLField(max_length=200, null=True, blank=True)
    related = models.ManyToManyField("self", blank=True, related_name="related", through="CourseRelated")
    slug = models.SlugField(blank=True, null=True)
    state = models.CharField(max_length=4, choices=PublishStateOptions.choices, default=PublishStateOptions.DRAFT)
    publish_timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager(blank=True)
    ratings = GenericRelation(Rating, related_query_name="course")
    category = models.ForeignKey(Category, related_name='courses', blank=True, null=True, on_delete=models.SET_NULL)
    updated = models.DateTimeField(auto_now=True)
    price  = models.DecimalField(decimal_places=2, max_digits=20, default=39.99,  blank=True, null=True)
  
    
    objects = CourseManager()

    def __str__(self) -> str:
        return self.title

    def get_related_items(self):
        return self.courserelated_set.all()
    
    def get_status_css(self):
        if self.state == PublishStateOptions.LIVE:
            return 'bg-success'
        if self.state == PublishStateOptions.PENDING:
            return 'bg-warning'
        
        if self.state == PublishStateOptions.DRAFT:
            return 'bg-info'
        return 'bg-danger'
    
    def get_absolute_url(self):
        if self.is_basic:
            return f"/basics/{self.slug}/"
        if self.is_intermediate:
            return f"/intermediates/{self.slug}/"
        if self.is_advanced:
            return f"/advanced/{self.slug}/"
        if self.is_deep_dive:
            return f"/deep/{self.slug}/"
        if self.is_featured: 
            return f"/featured/{self.slug}"
        
        return f"/courses/{self.slug}"
       

    def get_rating_avg(self):
        return Course.objects.filter(id=self.id).aggregate(Avg("ratings__value"))

    def get_rating_spread(self):
        return Course.objects.filter(id=self.id).aggregate(max=Max("ratings__value"), min=Min("ratings__value"))
    
    @property
    def is_published(self):
        return self.active
    
    @property
    def is_featured(self):
        return self.level == self.CourseLevelOptions.FEATURED
    
    @property
    def is_basic(self):
        return self.level == self.CourseLevelOptions.BASIC
    
    @property
    def is_intermediate(self):
        return self.level == self.CourseLevelOptions.INTERMEDIATE
   
    @property
    def is_advanced(self):
        return self.level == self.CourseLevelOptions.ADVANCED
    
    @property
    def is_deep_dive(self):
        return self.level == self.CourseLevelOptions.DEEP

    def get_video_id(self):
         pass
    

    
class CourseItemQuerySet(models.QuerySet):
    def published(self):
        now = timezone.now()
        return self.filter(
            course__state = PublishStateOptions.LIVE,
            course__publish_timestamp__lte= now,
        )

class CourseItemManager(models.Manager):
    def get_queryset(self):
        return CourseItemQuerySet(self.model, using=self._db)
    
    def published(self):
        return self.get_queryset().published()

class CourseItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CourseItemManager()

    class Meta:
        ordering = ['order', '-timestamp']


class CourseRelated(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    related = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='related_item')
    order = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)



pre_save.connect(publish_state_pre_save, sender=Course)
pre_save.connect(unique_slugify_pre_save, sender=Course)



