from django.db import models
from instructors.models import Instructor
from courses.models import Course
# Create your models here.
class Experience(models.Model):
    name = models.CharField(max_length=220)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Goal(models.Model):
    name = models.CharField(max_length=220)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Requirement(models.Model):
    name = models.CharField(max_length=220)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)