from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Article, Comment


class FilterCommentSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class RecursiveSerializer(serializers.Serializer):

    def to_representation(self, instance):
        serializer = CommentSerializer(instance, context=self.context)
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    '''Сериализатор для комментария к новости'''
    username = serializers.CharField(source='author.username')
    children = RecursiveSerializer(many=True, allow_null=True)

    def get_depth(self, obj):
        return obj.depth

    def validate(self, attrs):
        instance = Comment(**attrs)
        instance.clean()
        return attrs

    class Meta:
        list_serializer_class = FilterCommentSerializer
        model = Comment
        fields = ('id', 'username', 'content', 'created_at', 'depth', 'children')


class CommentCreateSerializer(serializers.ModelSerializer):
    '''Сериализатор для создания новостей'''

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        instance.author = self._context['request'].user
        instance.save()
        return instance

    class Meta:
        model = Comment
        fields = ('content', 'article', 'parent')


class ArticleSerializer(serializers.ModelSerializer):
    '''Сериализатор для новостей'''
    class Meta:
        model = Article
        fields = '__all__'


class ArticleDetailSerializer(serializers.ModelSerializer):
    '''Сериализатор для конкретной новости с комментариями'''
    comments = CommentSerializer(many=True)

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'created_at', 'author', 'comments')



class UserBanSerializer(serializers.ModelSerializer):
    '''Сериализатор состояния "is_banned" пользователя'''
    class Meta:
        model = get_user_model()
        fields = ('is_banned', )
