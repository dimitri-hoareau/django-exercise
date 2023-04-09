from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
 
from sales.models import Article, Sale
from sales.serializers import ArticleSerializer
 
class ArticleViewset(ModelViewSet):
    """
    Viewset for the Article model, used to handle HTTP requests and responses related to Articles.
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
 
    serializer_class = ArticleSerializer
 
    def get_queryset(self):
        return Article.objects.all()