from django.contrib import admin
from tags.admin import TaggedItemInline
from .models import Course, CourseItem, CourseRelated
from targets.models import Goal, Experience, Requirement


# Register your models here.


class CourseSectionInline(admin.TabularInline):
    model = CourseItem
    extra = 0 

class CourseGoals(admin.TabularInline):
    model = Goal
    extra = 0 

class CourseRequirements(admin.TabularInline):
    model = Requirement
    extra = 0 

class CourseExperience(admin.TabularInline):
    model = Experience
    extra = 0 


class CourseRelatedInline(admin.TabularInline):
    model = CourseRelated
    fk_name = 'course'
    extra = 0

class CourseItemInline(admin.TabularInline):
    model = CourseItem
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseRelatedInline, CourseItemInline, CourseExperience, CourseRequirements
    , CourseGoals]
    fields = [
        'title',
        'description',
        'slug',
        'state',
        'active',
        'price',
        'category',
        'instructor',
        'video_url',
        'headline',
        'tags',
        'lead',
        'cover_image',
    ]
    class Meta:
        model = Course
    
    def get_queryset(self, request):
        return Course.objects.all()
    
admin.site.register(Course, CourseAdmin)

    