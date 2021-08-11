from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models.signals import pre_save

from tags.models import TaggedItem
from readux.db.receivers import unique_slugify_pre_save
# Create your models here.
class ProjectCategory(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.SET_NULL, blank=True, null=True)
    title = models.CharField(max_length=220)
    slug = models.SlugField(blank=True, null=True)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tags = GenericRelation(TaggedItem, related_query_name="project_category")


    def get_absolute_url(self):
        return f"/project_categories/{self.slug}/"
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'

    
pre_save.connect(unique_slugify_pre_save, sender=ProjectCategory)
