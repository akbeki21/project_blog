from rest_framework import serializers

from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    
    def _get_image_url(self, obj):
        """method to get images url"""
        request   = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        
        return representation


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    
    def _get_image_url(self, obj):
        request   = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        return representation


class CategorySerializer(serializers.ModelSerializer):
    products = ProductListSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = "__all__"




class CreateUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ('calories', 'fats', 'carbohydrates', 'categories', 'proteins')


