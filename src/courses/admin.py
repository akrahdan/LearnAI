from django.contrib import admin
from tags.admin import TaggedItemInline
from .models import Course, CourseItem, CourseRelated


# Register your models here.


class CourseSectionInline(admin.TabularInline):
    model = CourseItem
    extra = 0 


class CourseRelatedInline(admin.TabularInline):
    model = CourseRelated
    fk_name = 'course'
    extra = 0

class CourseItemInline(admin.TabularInline):
    model = CourseItem
    extra = 0

class CourseAdmin(admin.ModelAdmin):
    inlines = [CourseRelatedInline, CourseItemInline]
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
        'tags',
        'lead',
    ]
    class Meta:
        model = Course
    
    def get_queryset(self, request):
        return Course.objects.all()
    
admin.site.register(Course, CourseAdmin)

    