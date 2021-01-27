from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import CategoriesList, ProductViewSet


router = DefaultRouter()
router.register('', ProductViewSet)

# products = ProductViewSet.as_view({
#     'get': 'list',
#     'put': 'update',
#     'patch': 'partial_update',
#     'post': 'create',
#     'delete': 'destroy',
# })

urlpatterns = [
    path('categories/', CategoriesList.as_view()),
    path('', include(router.urls)),
]