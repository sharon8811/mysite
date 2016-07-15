from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
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
    user = models.ForeignKey(User, null=True, blank=True)

    def __str__(self):
        return "Article id:%s, name: %s" % (str(self.id), self.name)

    def imgsum(self):
        imgs = ArticleImages.objects.filter(article=self.id)
        if imgs:
            return len(imgs) + 1
        else:
            return 0

class ArticleImages(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.TextField()

    def __str__(self):
        return "Article image id: %s \n Image DATA: " % (str(self.article.id), self.image)


class ArticleFakeImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="/home/sharon/mysite/static/uploads/images/")

    def __str__(self):
        return "Article fake image id: %s Image path: %s" %(str(self.article.id), self.image.path)
