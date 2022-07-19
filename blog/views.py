from django.utils.http import urlsafe_base64_encode
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, FormView
from .models import Article
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse

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
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=data))
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
                        
            # mail = form.send_mail(
            #     subject_template_name="Change Password",
            #     email_template_name="",
            #     context={form},
            #     from_email="bouyesophonie@gmail.com",
            #     to_email=form.
            #     )

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