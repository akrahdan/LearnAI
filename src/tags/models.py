from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import pre_save

# Create your models here.

class TaggedItemManager(models.Manager):
    def unique_list(self):
        tags_set = set(self.get_queryset().values_list('tag', flat=True))
        tag_list = sorted(list(tags_set))
        return tag_list

class TaggedItem(models.Model):
    tag = models.SlugField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    objects = TaggedItemManager()

    @property
    def slug(self):
        return self.tag
    
def lowercase_tag_pre_save(sender, instance, *args, **kwargs):
    instance.tag = f"{instance.tag}".lower()

pre_save.connect(lowercase_tag_pre_save, sender=TaggedItem)




