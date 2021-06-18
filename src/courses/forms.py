from django import forms
from django.forms import widgets
from taggit.forms import TagWidget

from .models import Course


class CreateCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'instructor',
            'order',
            'level',
            'video_url',
            'category',
            'price',
            'tags',
        ]
    
class UpdateCourseForm(forms.ModelForm):
    video_url = forms.URLField(max_length=200, widget=forms.TextInput, help_text="Please enter the url of the page")
    class Meta:
        model = Course
        fields = [
         
            'video_url',

        ]
    
class FormRequirements(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'tags'
        ]
        widgets = {
            'tags': TagWidget
        }
