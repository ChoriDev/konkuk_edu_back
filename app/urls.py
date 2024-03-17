from django.urls import include, path
from rest_framework import routers
from app.views import ItemList
from app.views import ItemDetail
# from app.views import ItemViewSet

# APIView로 구현한 CURD에 대한 URL
urlpatterns = [
    path('item/', ItemList.as_view()),
    path('item/<int:pk>', ItemDetail.as_view())
]


# ViewSet으로 구현한 CRUD에 대한 URL
# router = routers.DefaultRouter()
# router.register('items', ItemViewSet)

# urlpatterns = [
#     path('', include(router.urls)),
# ]