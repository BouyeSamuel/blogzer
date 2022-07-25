from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.detail import SingleObjectMixin
from .models import Article, Category, Like
from django.contrib.auth import login, authenticate, logout
from .forms import CommentFormAuthUser, CommentFormNotAuthUser, NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.edit import FormMixin
import json
from django.core import serializers

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


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            email = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=email))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    template_email = "blog/email/email.txt"
                    c = {
                        "email": user.email,
                        "domain": '127.0.0.1:8000',
                        'site_name': 'Blogzer',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": 'http'
                    }
                    
                    email = render_to_string(template_email, c)
                    
                    try:
                        send_mail(subject=subject, message=email, from_email="blogzer@mail.com",recipient_list=[user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("password_reset_done")
    password_reset_form = PasswordResetForm()
    return render(request, template_name='blog/registration/password_reset.html', context={"password_reset_form":password_reset_form})
                        
class ArticleListView(ListView):
    model = Article
    template_name = 'blog/article_list.html'


class ArticleInterestCommentFormView(SingleObjectMixin, FormView, FormMixin):
    template_name = 'blog/article_detail.html'
    model = Article
    
    def get_form_class(self):
        if self.request.user.is_authenticated:
            self.form_class = CommentFormAuthUser
        else:
            self.form_class = CommentFormNotAuthUser
        return self.form_class
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        new_comment = None
        article = get_object_or_404(Article, slug=self.object.slug)
        
        comments = article.comments.all()
        print(comments)
        form = self.get_form()
        
        self.object = self.get_object()

        if not request.user.is_authenticated:
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.article = article
                new_comment.save()
                return super().form_valid(form)
        if form.is_valid():
            try:
                user = User.objects.filter(pk=request.user.pk).first()
            except User.DoesNotExist:
                print('user not exist')
            
            new_comment = form.save(commit=False)
            new_comment.username = user.username
            new_comment.email = user.email
            new_comment.article = article
            new_comment.save()
            # return new_comment
            return super().form_valid(form)
        # print(Article.objects.filter(pk=request.article.pk))
            # return print(f"Debug request {request.user.username}")
        else:
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse('article_detail', kwargs={'slug': self.object.slug})

class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['comments'] = self.get_object().comments.order_by('-created_at')
        context['categories'] = self.get_object().category.all()
        if self.request.user.is_authenticated:
            context['form'] = CommentFormAuthUser()
        else:
            context['form'] = CommentFormNotAuthUser()
        return context
    
    
class ArticleView(View):

    def get(self, request, *arg, **kwargs):
        print('***** get')
        view = ArticleDetailView.as_view()
        return view(request, *arg, **kwargs)
    
    def post(self, request, *arg, **kwargs):
        print('***** post')
        view = ArticleInterestCommentFormView.as_view()
        return view(request, *arg, **kwargs)
    
class CategoryListView(ListView):
    model = Category
    template_name = 'blog/categories.html'
    
class CategoryDetailView(DetailView):
    model = Category
    template_name = 'blog/category.html'
    
    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['articles'] = Article.objects.filter(category=self.object)
        return context
    
    
def like_request(request):
    if request.method == "POST":
        article =   get_object_or_404(Article,pk=request.POST.get('article_pk'))
        user = get_object_or_404(User,pk=request.POST.get('user_pk'))
        
        likes = Like.objects.filter(article_id=article.pk)
        tempJson = serializers.serialize("json", likes)
        jsonObj = json.loads(tempJson)
        user_in_like = Like.objects.filter(user=user)
        if likes:
            print('*** like_obj')
            try:
                like_obj = Like.objects.get(article=article,user=user)
            except Like.DoesNotExist:
                like_obj = False
        
        if like_obj is False:
            new_like = Like.objects.create(article=article, user=user)
            new_like.save()
            liked = 'new'
            print('I have find bro I create a new') 
            return JsonResponse(jsonObj, safe=False)
        elif like_obj and like_obj.liked:
            # should false
            like_obj.liked = False
            like_obj.save()
            liked = 'false'
            # html = render_to_string('blog/article_detail.html', {'likes': likes, 'liked': liked})
            return JsonResponse(jsonObj, safe=False)
        elif like_obj and like_obj.liked is False:
            # should true            
            like_obj.liked = True
            like_obj.save()
            liked = 'true'
            # html = render_to_string('blog/article_detail.html', {'likes': likes, 'liked': liked})
            return JsonResponse(jsonObj, safe=False)

    return JsonResponse(jsonObj, safe=False)