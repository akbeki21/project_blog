from django.urls import path

from .views import *


# products = ProductViewSet.as_view({
#     'get': 'list',
#     'put': 'update',
#     'patch': 'partial_update',
#     'post': 'create',
#     'delete': 'destroy',
# }) 
urlpatterns = [
    path('recipes/', RecipeView.as_view({
    'get': 'list',
    'put': 'update',
    'patch': 'partial_update',
    'post': 'create',
    'delete': 'destroy',
})),
]