from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
 
from sales.models import Article, Sale
from sales.serializers import ArticleSerializer, SaleSerializer
 
class ArticleViewset(ModelViewSet):
    """
    Viewset for the Article model
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
 
    serializer_class = ArticleSerializer
 
    def get_queryset(self):
        return Article.objects.all()
    

class SaleViewset(ModelViewSet):
    """
    Viewset for the Sale model
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
 
    serializer_class = SaleSerializer
 
    def get_queryset(self):
        return Sale.objects.all()