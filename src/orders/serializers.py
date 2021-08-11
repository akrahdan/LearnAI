from rest_framework import serializers
from .models import Order, ProjectOrder

class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class ProjectOrderSerializzer(serializers.ModelSerializer):
    class Meta:
        model  = ProjectOrder
        fields = ['project']
        depth = 2