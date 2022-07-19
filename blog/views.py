from django.views.generic import ListView, DetailView, FormView
from .models import Article
from .forms import CommentForm

class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'

class CommentFormView(FormView):
    template_name = 'blog/article_list.html'
    form_class = CommentForm
    success_url = '/'