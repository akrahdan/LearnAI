from django.urls import path
from .views import CompleteOrderView, VerifyOwnership, MyProjectsView
urlpatterns = [
    path('complete/', CompleteOrderView.as_view(), name='complete_order'),
    path('endpoint/verify/ownership/', VerifyOwnership.as_view(), name='verify-ownership'),
    path('my_projects/', MyProjectsView.as_view()),

]