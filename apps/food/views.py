from rest_framework.parsers import MultiPartParser, FormParser

from .models import Dish
from core.viewsets import CoreViewSet
from .serializers import DishSerializer


class DishViewSet(CoreViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    parser_classes = (MultiPartParser, FormParser)



