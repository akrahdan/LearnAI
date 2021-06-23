from django.db import models
from courses.models import Course
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.
class ReviewRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rating = models.FloatField()
    review = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)