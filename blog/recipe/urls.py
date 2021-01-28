from django.urls import path

from .views import *

urlpatterns = [
    path('recipes/', RecipeViewSet.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'put': 'update',
        'delete': 'destroy'
    })),
]