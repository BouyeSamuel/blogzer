from django.db import models
from django.contrib.auth import User
from django.urls import reverse

class Article(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField()
    slug = models.SlugField(null=True)
    pub_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
    
    def get_absolute_url(self):
        return reverse("article_detail", kwargs={"pk": self.pk})
    

# class Comment(models.Model):
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.CharField()

# class Like(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)

# class Category(models.Model):
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)

# class Tag(models.Model):
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)