from django.shortcuts import render, redirect 
from django.contrib import messages
from .models import ReviewRating
from .forms import ReviewRatingForm

# Create your views here.
def submit_review(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
          reviews = ReviewRating.objects.get(user=request.user, course__id=id)
          form = ReviewRatingForm(request.POST, instance=reviews)
          form.save()
          messages.success(request, "Thank you. Your review has been updated")
          return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewRatingForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.course_id = id
                data.user = request.user
                data.save()
                
                messages.success(request, "Thank you. Your review has been submitted")
                return redirect(url)