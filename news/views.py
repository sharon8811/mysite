from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse
from .models import Article, ArticleImages


# Create your views here.
def index(request):
    if request.is_ajax():
        #return search
        if request.method == "POST":
            search_text = request.POST['search_text']
        else:
            search_text = ''
        if search_text != '':
            news = Article.objects.filter(name__icontains=search_text)
        else:
            news = ''
        return render_to_response('news/ajax_search.html', {'news': news})
    else:
        template_name = 'news/index.html'
        news_list = Article.objects.order_by('-date')
        return render(request, template_name,  {'news_list': news_list})


def article(request, article_id):
    template_name = 'news/article.html'
    arti = get_object_or_404(Article, pk=article_id)
    #image = ArticleImages.objects.get(article=arti.id)
    arti.views += 1
    arti.save()
    context = {'article': arti, 'image': "none"}
    return render(request, template_name, context)