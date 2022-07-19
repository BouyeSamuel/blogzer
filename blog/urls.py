from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import ArticleListView, ArticleDetailView
from . import views

urlpatterns = [
    path('<slug:slug>', ArticleDetailView.as_view(), name="article_detail"),
    path('', ArticleListView.as_view(), name="article_list"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)