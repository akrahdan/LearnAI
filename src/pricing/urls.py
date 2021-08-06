from django.urls import path
from .views import PricingTierOptions, CurrencyOptions, PricingView
urlpatterns = [
    path('tier/',PricingTierOptions.as_view()),
    path('create/', PricingView.as_view()),
    path('currency/', CurrencyOptions.as_view())
]