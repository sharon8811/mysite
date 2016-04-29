from django.conf.urls import url
from . import views

app_name = "news"

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^article/([0-9]+)/$', views.article, name='article'),
    url(r'^article/(?P<article_id>[0-9]+)/(?P<page>[0-9]+)/$', views.article, name='article_pages'),
    url(r'article/edit/(?P<article_id>[0-9]+)/$', views.editarticle, name='edit_article'),
    url(r'article/edit/deleteimage/(?P<image_id>[0-9]+)/$', views.deleteimage, name='edit_delete_image'),
    url(r'article/edit/replaceimage/(?P<image_id>[0-9]+)/$', views.replaceimage, name='edit_replace_image'),
    url(r'article/edit/addimage/(?P<article_id>[0-9]+)/$', views.addimage, name='edit_add_image'),
    url(r'^author/(?P<author_name>[-."\'\w\s]+)/$', views.author, name='author'),
    url(r'^author/(?P<author_name>[-."\'\w\s]+)/(?P<page_to_return>[0-9]+)/$', views.author, name='author_page'),
    url(r'^submit/$', views.submit, name='submit'),
    url(r'^image/(?P<image_id>[0-9]+)/$', views.image, name='image'),
    url(r'^image/viewall/$', views.imagesviewall, name='imagesviewall'),
]
