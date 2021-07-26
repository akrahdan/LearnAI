# index.py
from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from taggit.models import Tag


# algoliasearch.register(Course)

@register(Tag)
class TagIndex(AlgoliaIndex):
    fields = ('name')
    settings = {'searchableAttributes': ['name']}
    index_name = 'tags_index'
