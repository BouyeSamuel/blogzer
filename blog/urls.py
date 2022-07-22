from urllib import request
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ArticleListView, ArticleView, CategoryListView, CategoryDetailView
from . import views

urlpatterns = [
    path('<slug:slug>', ArticleView.as_view(), name="article_detail"),
    # path('<slug:slug>', comment_request, name="article_detail_comment"),
    path('', ArticleListView.as_view(), name="article_list"),
    path('categories/', CategoryListView.as_view(), name="categories_list"),
    path('categories/<int:pk>', CategoryDetailView.as_view(), name="category_detail"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)