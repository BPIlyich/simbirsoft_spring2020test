from django.conf import settings
from django.contrib.auth.models import AbstractUser
# from django.core.exceptions import ValidationError
from django.db import models
from rest_framework.serializers import ValidationError


# TODO лучше вынести в отдельный APP
class User(AbstractUser):
    '''Custom user model'''
    email = models.EmailField(unique=True, blank=False)
    is_banned = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Article(models.Model):
    '''Article model'''
    title = models.CharField(max_length=120, verbose_name='Заголовок новости')
    content = models.TextField(verbose_name='Текст новости')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создано'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='news',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']


class Comment(models.Model):
    '''Comment model'''
    MAX_COMMENT_DEPTH = 5

    content = models.TextField(
        max_length=255,
        verbose_name='Текст комментария'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE,
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name='Родитель'
    )

    def clean(self):
        depth = 0
        model = self
        while model.parent:
            depth += 1
            model = model.parent
            if depth > self.MAX_COMMENT_DEPTH:
                print(depth)
                raise ValidationError(
                    'Превышен допустимый уровень вложенности комментариев - {}'.format(
                        self.MAX_COMMENT_DEPTH
                    )
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    @property
    def depth(self):
        depth = 0
        model = self
        while model.parent:
            depth += 1
            model = model.parent
        return depth

    depth.fget.short_description = 'Уровень вложенности комментария'

    def __str__(self):
        return '{:.20}'.format(self.content)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
