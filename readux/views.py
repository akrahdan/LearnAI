from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from allauth.account.views import SignupView
from courses.models import Course
from carts.models import Cart
def home_page(request):
    return render(request, 'app.html', {})

class CourseLeadView(SignupView):
    template_name = 'course_lead.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        qs = Course.objects.lead_course()
        if qs.exists():
            lead = qs.first()
            context = super().get_context_data(**kwargs)
            context['lead'] = lead
        return context
    
    def form_valid(self, form):

        course_id = self.request.POST.get('course_id')
        if course_id is not None:
            try:
                course_obj = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                print("Show message to user, course is gone?")
                return redirect("home")
            cart_obj, new_obj = Cart.objects.new_or_get(self.request)
            if course_obj in cart_obj.courses.all():
                cart_obj.courses.remove(course_obj)
                
            else:
                cart_obj.courses.add(course_obj) 
                

        return super().form_valid(form)
  
        
           
def pricing(request):
    return render(request, 'pricing.html', {})