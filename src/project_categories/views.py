from rest_framework.generics import ListAPIView
from .models import ProjectCategory
from .serializers import ProjectCategorySerializer
# Create your views here.

class ProjectCategoryView(ListAPIView):
    queryset = ProjectCategory.objects.all()
    serializer_class = ProjectCategorySerializer