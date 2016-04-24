from django.conf.urls import url
from . import views

app_name = "news"

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^article/([0-9]+)/$', views.article, name='article'),
    url(r'^author/(?P<author_name>[-\w\s]+)/$', views.author, name='author'),
]