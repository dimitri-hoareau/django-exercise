from django.urls import path, include

from rest_framework import routers
from sales.views import ArticleViewset, SaleViewset

router = routers.DefaultRouter(trailing_slash=False)
router.register('article', ArticleViewset, basename='article')
router.register('sale', SaleViewset, basename='sale')

urlpatterns = [
    path(
        "v1/",
        include(
            [
                path("", include(router.urls)),
            ]
        ),
    )
]
