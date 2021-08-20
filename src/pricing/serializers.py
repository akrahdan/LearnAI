from rest_framework import serializers
from .models import Pricing, ProjectPricing


class PricingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pricing
        fields = [
            'course',
            'currency',
            'amount'
        ]

class ProjectPricingSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectPricing
        fields = [
            'project',
            'currency',
            'amount'
        ]