from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
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
    ),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
