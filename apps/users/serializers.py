from rest_framework import serializers
from .models import CustomUser # Импортируйте вашу модель CustomUser
from apps.blog.serializers import CommentSerializer, PostListSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    posts = PostListSerializer(many=True, read_only=True, source='blog_posts') # Используем PostListSerializer
    comments = CommentSerializer(many=True, read_only=True, source='comment_set') # Вложенные комментарии

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'avatar', 'posts', 'comments']
        extra_kwargs = {
            'avatar': {'required': False},
        }