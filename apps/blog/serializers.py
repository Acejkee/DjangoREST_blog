from rest_framework import serializers
from .models import Category, Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.full_name') # Используем более descriptive имя

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'post', 'text', 'created_at']
        # exclude = ['post'] - не нужно, т.к. post используется в PostDetailSerializer
        extra_kwargs = {
            'post': {'required': False},
        }


class PostListSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.full_name')
    category_title = serializers.ReadOnlyField(source='category.title') # descriptive имя

    class Meta:
        model = Post
        fields = ['id', 'title', 'author_name', 'category_title', 'slug', 'created_at', 'content']


class PostDetailSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.full_name')
    category_title = serializers.ReadOnlyField(source='category.title')
    comments = CommentSerializer(many=True, read_only=True) # Вложенные комментарии
    comment_count = serializers.IntegerField(source='comments.count', read_only=True) # Количество комментариев

    class Meta:
        model = Post
        fields = ['id', 'title', 'author_name', 'category_title', 'slug' ,'created_at', 'content', 'comments', 'comment_count']


class CategoryListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка категорий"""
    post_count = serializers.IntegerField(source='posts.count', read_only=True) # Только количество постов

    class Meta:
        model = Category
        fields = ('id', 'title', 'post_count') # post_count


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального представления категории"""
    posts = PostListSerializer(many=True, read_only=True) # Полная информация о постах

    class Meta:
        model = Category
        fields = ('id', 'title', 'posts')




