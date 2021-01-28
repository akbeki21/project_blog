from django.db.models import Q
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view, action
from rest_framework.pagination import PageNumberPagination
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, viewsets, status, mixins
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError

from .permissions import IsAuthor
from .models import *
from .serializers import *



class MyPaginationClass(PageNumberPagination):
    page_size = 2


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = MyPaginationClass

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [permissions.IsAuthor]
        else:
            permissions = [permissions.IsAuthenticated]
        return [permission() for permission in permissions]

    def retrieve(self, request, pk):
        if request.method == 'GET':
            queryset = self.filter_queryset((self.get_queryset()))
            obj = self.get_object()
            obj.save()
        return super().retrieve(request)


    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You deleted recipe')


    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     weeks_count = int(self.request.query_params.get('days',0))
    #     print(self.request.query_params)
    #     if weeks_count > 0:
    #         start_date = timezone.now() - timedelta(days=weeks_count)
    #         queryset = queryset.filter(created_at__gte=start_date)
    #     return queryset

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = RecipeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostImageView(generics.ListCreateAPIView):
    queryset = RecipeImage.objects.all()
    serializer_class = RecipeImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You deleted the comment')


class LikeCreate(generics.CreateAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        recipe = Recipe.objects.get(pk=self.kwargs['pk'])
        return Like.objects.filter(author=user, recipe=recipe)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You liked this post')
        serializer.save(author=self.request.user, post=Post.objects.get(pk=self.kwargs['pk']))

