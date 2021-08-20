from django.urls import path
from .views import PricingTierView, CurrencyOptionsView, PricingView, ProjectPricingView
urlpatterns = [
    path('tier/',PricingTierView.as_view()),
    path('create/', PricingView.as_view()),
    path('project/create/', ProjectPricingView.as_view()),
    path('currency/', CurrencyOptionsView.as_view())
]