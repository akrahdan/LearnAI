from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, DetailView, View, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from allauth.account.views import PasswordChangeView

from accounts.models import Profile
from .forms import ProfileDetailChangeForm
from files.models import S3File
def signup(request):
    return render(request, 'accounts/sign-up.html')


def signin(request):
    return render(request, 'accounts/sign-in.html')

def forgotPassword(request):
    return render(request, 'accounts/forgot-password.html')

def terms(request):
    return render(request, 'accounts/terms-condition.html')

def deleteProfile(request):
    return render(request, 'accounts/delete-profile.html')


def linkedAccounts(request):
    return render(request, 'accounts/linked-accounts.html')
def notifications(request):
    return render(request, 'accounts/notifications.html')

def editProfile(request):
    return render(request, 'accounts/profile-edit.html')

class ProfileEditView(UpdateView):
    form_class = ProfileDetailChangeForm
    model = Profile
    template_name = 'accounts/profile-edit.html'
    success_url = reverse_lazy('account_profile')

    def get_object(self):
        qs = Profile.objects.filter(user=self.request.user)
        return qs.first()

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileEditView, self).get_context_data(*args, **kwargs)
        user = self.request.user
        qs = S3File.objects.filter(user=user)
        if qs.exists():
            avatar = qs.last().get_download_url()
            context['avatar'] = avatar
        
        
        return context

def security(request):
    return render(request, 'accounts/security.html')

class SecurityView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'accounts/security.html'
    success_url = reverse_lazy('home')

def privacy(request):
    return render(request, 'accounts/profile-privacy.html')

def socialProfile(request):
    return render(request, 'accounts/social-profile.html')
