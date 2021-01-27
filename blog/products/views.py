from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import permissions, viewsets, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.response import Response

from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend

from .models import *
from .serializers import *
# from .filters import ProductFilter


class MyPaginationClass(PageNumberPagination):
    page_size = 1


class CategoriesList(ListAPIView):
    queryset         = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset  = Product.objects.all()
    pagination_class = MyPaginationClass
    filter_backends  = [DjangoFilterBackend]
    # filterset_fields = ['categories']
    # filter_class = ProductFilter


    def get_serializer_class(self):
        if  self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductSerializer
        return CreateUpdateProductSerializer


    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            permissions = []
        else:
            permissions = [permissions.IsAdminUser]
        return [permission() for permission in permissions]


    @action(methods=['get'], detail=False)
    def search(self, request):
        q  = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(Q(product_name__icontains=q))
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



