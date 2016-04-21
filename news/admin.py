from django.contrib import admin
from .models import Article, ArticleImages
# Register your models here.


class ArticleImagesInline(admin.StackedInline):
    model = ArticleImages


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'writer')
    inlines = [ArticleImagesInline]

admin.site.register(Article, ArticleAdmin)