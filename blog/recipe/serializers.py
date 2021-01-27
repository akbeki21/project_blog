from rest_framework import serializers

from .models import *


class RecipeSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        representation['images'] = RecipeImageSerializer(instance.images.all(), many=True, context=self.context).data
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        recipe = Recipe.objects.create(**validated_data)
        return recipe


class RecipeDetailSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['images'] = RecipeImageSerializer(instance.images.all(), many=True, context=self.context).data
        representation['comment'] = CommentSerializer(instance.comment.all(), many=True).data
        return representation

    def get_likes(self, post):
        return Like.objects.filter(recipe=recipe).count()


class RecipeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeImage
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
        return representation


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'