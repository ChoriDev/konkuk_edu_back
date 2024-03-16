from rest_framework.response import Response
from rest_framework import viewsets

from app.models import Item
from app.serializers import ItemSerializer

# Create your views here.

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer