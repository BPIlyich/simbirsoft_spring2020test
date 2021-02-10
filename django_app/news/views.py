from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, generics

from .models import Article, Comment
from .serializers import (
    ArticleSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    UserBanSerializer
)
from .permissions import IsNotBanned


User = get_user_model()

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            self.permission_classes = [permissions.AllowAny]
        elif self.action == 'retrieve':
            self.permission_classes = [permissions.IsAuthenticated]
        else:
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            self.serializer_class = ArticleDetailSerializer
        else:
            self.serializer_class  = ArticleSerializer
        return super().get_serializer_class()


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    http_method_names = ['post', 'delete']

    def perform_create(self, serializer):
        author = self.request.user
        return serializer.save(author=author)

    def get_serializer_class(self):
        if self.action == 'destroy':
            self.serializer_class = CommentSerializer
        else:
            self.serializer_class = CommentCreateSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [permissions.IsAuthenticated, IsNotBanned]
        elif self.action == 'destroy':
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()


class UpdateBanUserView(generics.UpdateAPIView):
    '''Блокировка / Разблокировка пользователя'''
    queryset = User.objects.all()
    serializer_class = UserBanSerializer
    permission_classes = [permissions.IsAdminUser]
