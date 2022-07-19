from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from .models import Article
from django.contrib.auth import login
from .forms import NewUserForm
from django.contrib import messages

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,"Registration Successful")
            return redirect("article_list")
        messages.error(request, "Unsuccessful registration, cause invalid information")
    form = NewUserForm()
    return render(request, template_name='blog/register.html', context={"register_form":form})
class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'


# class CommentFormView(FormView):
#     template_name = 'blog/article_list.html'
#     form_class = CommentForm
#     success_url = '/'