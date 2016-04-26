from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.


class Article(models.Model):
    name = models.CharField(max_length=500)
    writer = models.CharField(max_length=50)
    date = models.DateTimeField('date published', default=timezone.now())
    short_text = models.TextField()
    text = RichTextField()
    views = models.IntegerField(default=0)


class ArticleImages(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.TextField()
