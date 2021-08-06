from django.db import models

from courses.models import Course
from instructors.models import Instructor

# Create your models here.


class Pricing(models.Model):
    class PricingTierOptions(models.TextChoices):
        TIER1 = (50, '50')
        TIER2 = (100, '100')
        TIER3 = (200, '200')
        TIER4 = (300, '300')
        TIER5 = (400, '400')
        TIER6 = (500, '500')

    class CurrencyOptions(models.TextChoices):
        CEDIS = ('GHS', 'GHS')
        DOLLAR = ('USD', 'USD')
        POUND = ('GBP', 'GBP')
    amount = models.CharField(
        max_length=5, choices=PricingTierOptions.choices, default=PricingTierOptions.TIER1)
    currency = models.CharField(
        max_length=4, choices=CurrencyOptions.choices, default=CurrencyOptions.DOLLAR)
    course = models.OneToOneField(Course, on_delete=models.CASCADE, related_name='pricing')
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
   
