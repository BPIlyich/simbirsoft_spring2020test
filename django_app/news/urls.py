from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CommentViewSet, UpdateBanUserView

urlpatterns = [
    path('user/ban/<int:pk>/', UpdateBanUserView.as_view()),
]

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'comments', CommentViewSet)
urlpatterns += router.urls
