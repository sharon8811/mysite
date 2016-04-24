from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse
from .models import Article, ArticleImages
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def index(request):
    if request.is_ajax():
        #return search
        if request.method == "POST":
            search_text = request.POST['search_text']
        else:
            search_text = ''
        if search_text != '':
            news = Article.objects.filter(Q(name__icontains=search_text) | Q(writer__icontains=search_text)).order_by('-date')
        else:
            news = ''
        return render_to_response('news/ajax_search.html', {'news': news})
    else:
        template_name = 'news/index.html'
        news_list = Article.objects.order_by('-date')
        npaginator = Paginator(news_list, 2)  # Show 25 contacts per page

        page = request.GET.get('page')
        try:
            news = npaginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            news = npaginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            news = npaginator.page(npaginator.num_pages)

        return render(request, template_name,  {'news_list': news, 'author_page': False})


def article(request, article_id):
    template_name = 'news/article.html'
    arti = get_object_or_404(Article, pk=article_id)
    #image = ArticleImages.objects.get(article=arti.id)
    arti.views += 1
    arti.save()
    context = {'article': arti, 'image': "none"}
    return render(request, template_name, context)


def author(request, author_name):
    template_name = 'news/index.html'
    news_list = Article.objects.filter(writer=author_name).order_by('-date')
    npaginator = Paginator(news_list, 2)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        news = npaginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = npaginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = npaginator.page(npaginator.num_pages)

    return render(request, template_name, {'news_list': news, 'author_page': True, 'author_name': author_name})
