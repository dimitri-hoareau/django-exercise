from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
 
from sales.models import Article, Sale
from sales.serializers import ArticleSerializer, SaleSerializer

class CreateOnly(BasePermission):
    """
    Custom permission class that allows only POST requests.
    """
    def has_permission(self, request, view):
        return request.method == 'POST'
    
class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission class that allows owners to edit their own sales but only allows
    read-only access to other users.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for all requests, so we'll always allow GET, HEAD, and OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the author of the sale.
        return obj.author == request.user
 
class ArticleViewset(ModelViewSet):
    """
    Viewset for the Article model
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, CreateOnly]
 
    serializer_class = ArticleSerializer
 
    def get_queryset(self):
        return Article.objects.all()
    

class SaleViewset(ModelViewSet):
    """
    Viewset for the Sale model
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = SaleSerializer
 
    serializer_class = SaleSerializer
 
    def get_queryset(self):
        return Sale.objects.all()
    
    def perform_create(self, serializer):
        """
        Associate the current user with the created sale.
        """
        author = serializer.validated_data.get('author', None)
        if author is None:
            author = self.request.user
        serializer.save(author=author)