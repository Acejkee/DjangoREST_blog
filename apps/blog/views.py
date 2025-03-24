from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from .models import Post, Category, Comment
from .serializers import (
    PostListSerializer, PostDetailSerializer,
    CategoryListSerializer, CategoryDetailSerializer,
    CommentSerializer
)


class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.user.is_staff # Проверка на автора или админа



class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class CommentPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    pagination_class = PostPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly] # Упрощаем permissions

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.request.query_params.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        if not (self.request.user == instance.author or self.request.user.is_staff):
            self.permission_denied(self.request) # Используем permission_denied
        serializer.save()

    def perform_destroy(self, instance):
        if not (self.request.user == instance.author or self.request.user.is_staff):
            self.permission_denied(self.request)
        instance.delete()


class CategoryViewSet(viewsets.ReadOnlyModelViewSet): # ReadOnly, т.к. категории не изменяются через API
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategoryListSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            return Comment.objects.filter(post_id=post_pk) # Фильтруем по посту
        return Comment.objects.all() # Все комментарии


    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        if post_pk:
            try:
                post = Post.objects.get(pk=post_pk)
                serializer.save(author=self.request.user, post=post)
            except Post.DoesNotExist:
                return Response({'detail': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
           return Response({'detail': 'post_pk is required for creating a comment'}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        instance = self.get_object()
        if not (self.request.user == instance.author or self.request.user.is_staff):
            self.permission_denied(self.request)
        serializer.save()



    def perform_destroy(self, instance):
        if not (self.request.user == instance.author or self.request.user.is_staff):
            self.permission_denied(self.request)
        instance.delete()
