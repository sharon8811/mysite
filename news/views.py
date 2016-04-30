import base64
import StringIO
from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SubmitArticle
from .models import Article, ArticleImages
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse


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

        return render(request, template_name,  {'news_list': news, 'author_page': False, 'page': page})


def article(request, article_id, page=None):
    template_name = 'news/article.html'
    arti = get_object_or_404(Article, pk=article_id)
    images = ArticleImages.objects.filter(article=arti.id)
    text = arti.text
    if len(images) > 0:
        imagenum = 1
        for image in images:
            text = text.replace("{{ images.image" + str(imagenum) + " }}", '<img src="/news/image/' + str(image.id) + '/" style="width:750px;">')
            imagenum += 1
    arti.views += 1
    arti.save()
    context = {'article': arti, 'image': "none", 'page': page, 'text': text}
    return render(request, template_name, context)


def author(request, author_name, page_to_return=None):
    template_name = 'news/index.html'
    news_list = Article.objects.filter(writer=author_name).order_by('-date')
    npaginator = Paginator(news_list, 5)  # Show 5 per page

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
            numberofimages = int(request.POST['articlefakeimage_set-TOTAL_FORMS'])
            for number in range(numberofimages):
                if 'articlefakeimage_set-' + str(number) + '-image' in request.FILES:
                    newimagetosave = ArticleImages()
                    newimagetosave.article = newart
                    d = StringIO.StringIO()
                    filee = request.FILES['articlefakeimage_set-' + str(number) + '-image']
                    base64.encode(filee, d)
                    s = d.getvalue()
                    newimagetosave.image = "data:%s;base64,%s" % (filee.content_type, s)
                    newimagetosave.save()

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


def image(request, image_id):
    img = get_object_or_404(ArticleImages, pk=image_id)
    _, imgstr = img.image.split(',')
    pic = decode_base64(imgstr)
    return HttpResponse(pic, content_type='image/png')


def decode_base64(data):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    missing_padding = 4 - len(data) % 4
    if missing_padding:
        data += b'='* missing_padding
    return base64.decodestring(data)


@user_passes_test(lambda u: u.is_superuser)
def imagesviewall(request):
    imgs = ArticleImages.objects.all()
    template_name = 'news/viewall.html'
    return render(request, template_name, {'images': imgs})


@user_passes_test(lambda u: u.is_superuser)
def editarticle(request, article_id):
    if request.method == "POST":
        form = SubmitArticle(request.POST)
        if form.is_valid():
            article_to_change = get_object_or_404(Article, pk=article_id)
            article_to_change.name = request.POST['name']
            article_to_change.writer = request.POST['writer']
            article_to_change.short_text = request.POST['short_text']
            article_to_change.text = request.POST['text']
            article_to_change.save()
            return HttpResponseRedirect("/news/", {'msg': "Artice updated successfully"})
    else:
        template = "news/edit.html"
        article_to_edit = get_object_or_404(Article, pk=article_id)
        article_images = ArticleImages.objects.filter(article=article_to_edit)
        form = SubmitArticle(instance=article_to_edit)
        return render(request, template, {'article': article_to_edit, 'images': article_images, 'user_form': form})


@user_passes_test(lambda u: u.is_superuser)
def deleteimage(request, image_id):
    img = get_object_or_404(ArticleImages, pk=image_id)
    article_id = img.article_id
    img.delete()
    return HttpResponseRedirect("/news/article/edit/" + str(article_id) + "/", {'msg': "Image deleted successfully"})


@user_passes_test(lambda u: u.is_superuser)
def replaceimage(request, image_id):
    img = get_object_or_404(ArticleImages, pk=image_id)
    article_id = img.article_id

    d = StringIO.StringIO()
    filee = request.FILES['replaceimage']
    base64.encode(filee, d)
    s = d.getvalue()
    img.image = "data:%s;base64,%s" % (filee.content_type, s)
    img.save()

    return HttpResponseRedirect("/news/article/edit/" + str(article_id) + "/", {'msg': "Image updated successfully"})


@user_passes_test(lambda u: u.is_superuser)
def addimage(request, article_id):
    articletoaddimage = get_object_or_404(Article, pk=article_id)
    img = ArticleImages()
    img.article = articletoaddimage

    d = StringIO.StringIO()
    filee = request.FILES['addimage']
    base64.encode(filee, d)
    s = d.getvalue()
    img.image = "data:%s;base64,%s" % (filee.content_type, s)
    img.save()

    return HttpResponseRedirect("/news/article/edit/" + str(articletoaddimage.id) + "/", {'msg': "Image added successfully"})


@user_passes_test(lambda u: u.is_superuser)
def deletearticle(request, article_id):
    articletodelete = get_object_or_404(Article, pk=article_id)
    articletodelete.delete()
    if request.GET['back']:
        return HttpResponseRedirect(request.GET['back'])
    else:
        return HttpResponseRedirect("/news/")


@user_passes_test(lambda u: u.is_superuser)
def adminshowall(request, msg=None):
    articles = Article.objects.all().order_by('-date')
    return render(request, "news/adminviewallarticles.html", {'articles': articles, 'msg': msg})

