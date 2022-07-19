from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from .models import Article
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

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

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"You are logged now {username}")
                return redirect("article_list")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password re-enter")
    form = AuthenticationForm()
    return render(request, template_name="blog/login.html", context={"login_form": form})

def logout_request(request):
    logout(request)
    messages.success(request, "Your are successful logout")
    return redirect("article_list")

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