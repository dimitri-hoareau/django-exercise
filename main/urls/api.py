from django.urls import path, include

from rest_framework import routers
from sales.views import ArticleViewset

router = routers.DefaultRouter(trailing_slash=False)
router.register('article', ArticleViewset, basename='article')

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
