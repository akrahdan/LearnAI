from algoliasearch_django import AlgoliaIndex
from algoliasearch_django.decorators import register
from .models import Instructor


# algoliasearch.register(Course)

@register(Instructor)
class InstructorIndex(AlgoliaIndex):
    fields = ('first_name', 'last_name', 'id', 'avatar', 'user')
    settings = {'searchableAttributes': ['first_name']}
    index_name = 'instructor_index'
