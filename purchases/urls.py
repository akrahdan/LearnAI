from django.urls import path
from .views import CompletePurchaseView
urlpatterns = [
    path('<complete/', CompletePurchaseView.as_view(), name='complete_purchase')
]