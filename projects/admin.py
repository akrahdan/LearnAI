from django.contrib import admin
from .models import  ( TitleDescription, 
LearningOutCome, Testimonial, Project, 
ProjectRelated, Syllabus, ProjectSection )



class ProjectRelatedInline(admin.TabularInline):
    model = ProjectRelated
    fk_name = 'project'
    extra = 0

class LearningOutcomeInline(admin.TabularInline):
    model = LearningOutCome
    fk_name = 'project'
    extra = 0

class IncludesInline(admin.TabularInline):
    model = TitleDescription
    fk_name = 'project'
    extra = 0

class SyllabusInline(admin.TabularInline):
    model = Syllabus
    extra = 0
    


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectRelatedInline, LearningOutcomeInline, IncludesInline, SyllabusInline]
    
    class Meta:
        model = Project
    
    def get_queryset(self, request):
        return Project.objects.all()
admin.site.register(Project, ProjectAdmin)
admin.site.register(Testimonial)
admin.site.register(ProjectSection)

# Register your models here.
