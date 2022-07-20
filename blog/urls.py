from urllib import request
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ArticleListView, ArticleDetailView, ArticleView
from . import views

urlpatterns = [
    path('<slug:slug>', ArticleView.as_view(), name="article_detail"),
    # path('<slug:slug>', comment_request, name="article_detail_comment"),
    path('', ArticleListView.as_view(), name="article_list"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)