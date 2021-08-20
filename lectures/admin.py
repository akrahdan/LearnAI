from django.contrib import admin
from .models import Lecture, Section
# Register your models here.

admin.site.register(Section)

admin.site.register(Lecture)