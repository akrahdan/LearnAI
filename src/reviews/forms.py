from .models import ReviewRating
from django import forms

class ReviewRatingForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = [
            'rating',
            'review',
        ]