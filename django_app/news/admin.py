from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
from .models import Article, Comment  #, User

admin.site.register(Article)
admin.site.register(Comment)
# admin.site.register(User, UserAdmin)
