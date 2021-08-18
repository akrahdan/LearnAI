from rest_framework import serializers
from .models import Order, ProjectOrder
from projects.serializers import ProjectSerializer
class CreateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = '__all__'


class ProjectOrderSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    class Meta:
        model  = ProjectOrder
        fields = ['project']
        depth = 2