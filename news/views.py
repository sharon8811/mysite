from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse
from .forms import SubmitArticle
from .models import Article, ArticleImages
from django.utils import timezone
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
        npaginator = Paginator(news_list, 5)  # Show 25 contacts per page

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


def article(request, article_id, page=None):
    template_name = 'news/article.html'
    arti = get_object_or_404(Article, pk=article_id)
    #image = ArticleImages.objects.get(article=arti.id)
    arti.views += 1
    arti.save()
    context = {'article': arti, 'image': "none", 'page': page}
    return render(request, template_name, context)


def author(request, author_name, page_to_return=None):
    template_name = 'news/index.html'
    news_list = Article.objects.filter(writer=author_name).order_by('-date')
    npaginator = Paginator(news_list,5)  # Show 25 contacts per page

    page = request.GET.get('page')
    try:
        news = npaginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news = npaginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news = npaginator.page(npaginator.num_pages)

    return render(request, template_name, {'news_list': news, 'author_page': True, 'author_name': author_name, 'page': page_to_return})


def submit(request):
    if request.method == 'POST':
        form = SubmitArticle(request.POST)
        if form.is_valid():
            newart = Article(name=request.POST['name'], writer=request.POST['writer'], short_text=request.POST['short_text'], text=request.POST['text'], date=timezone.now(), views=0)
            newart.save()
            template_name = 'news/submit.html'
            context = {'user_form': form, 'err': '', 'suc': True}
            return render(request, template_name, context)
        else:
            template_name = 'news/submit.html'
            context = {'user_form': form, 'err': 'Please fill in all the fields'}
            return render(request, template_name, context)
    else:
        template_name = 'news/submit.html'
        form = SubmitArticle()
        context = {'user_form': form, 'err': ''}
        return render(request, template_name, context)
