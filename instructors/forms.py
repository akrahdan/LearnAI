from django import forms
from .models import Instructor
from taggit.forms import TagWidget
class InstructorForm(forms.ModelForm):

    class Meta:
        model = Instructor
        fields = [
            'first_name',
            'last_name',
            'description',
            'phone',
            'tags'
        ]

        widgets = {
            'tags': TagWidget
        }