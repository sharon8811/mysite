from django.conf.urls import url
from . import views

app_name = "news"

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^article/([0-9]+)/$', views.article, name='article'),
    url(r'^article/(?P<article_id>[0-9]+)/(?P<page>[0-9]+)/$', views.article, name='article_pages'),
    url(r'^author/(?P<author_name>[-."\'\w\s]+)/$', views.author, name='author'),
    url(r'^author/(?P<author_name>[-."\'\w\s]+)/(?P<page_to_return>[0-9]+)/$', views.author, name='author_page'),
    url(r'^submit/$', views.submit, name='submit'),
]
