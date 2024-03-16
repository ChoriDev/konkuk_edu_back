from django.urls import include, path
from rest_framework import routers
from app.views import ItemViewSet

router = routers.DefaultRouter()
router.register('items', ItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
]