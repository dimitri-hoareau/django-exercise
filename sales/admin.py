from django.contrib import admin

from sales.models import ArticleCategory, Article, Sale

admin.site.register(ArticleCategory)
admin.site.register(Article)
admin.site.register(Sale)
