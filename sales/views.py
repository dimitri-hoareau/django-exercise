from django.shortcuts import render
from django.db.models import F, FloatField, Sum
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
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
    filter_backends = [OrderingFilter]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        queryset = Sale.objects.all()

        article_id = self.request.GET.get('article_id')
        if article_id is not None:
            # Filter by article_id
            queryset = queryset.filter(article_id=article_id)

            # Sort the results in descending order by the total_selling_price 
            queryset = queryset.annotate(
                total_selling_price=Sum(F('quantity') * F('unit_selling_price'), output_field=FloatField())
            ).order_by('-total_selling_price')

            # Get the total of total_selling_price
            total_of_total_selling_price = queryset.aggregate(
                total_selling_price=Sum(F('quantity') * F('unit_selling_price'), output_field=FloatField())
            )
            # Set the value as an attribute
            self.total_of_total_selling_price = total_of_total_selling_price['total_selling_price']

            # Calculate the profit
            total_of_total_cost_price =  queryset.annotate(
                total_selling_price=Sum(F('quantity') * F('unit_selling_price'), output_field=FloatField()),
                manufacturing_cost=F('article__manufacturing_cost'),
                total_cost_price=F('quantity') * F('article__manufacturing_cost')
            )
 
            total_of_total_cost_price = total_of_total_cost_price.aggregate(total_cost_price=Sum(F('total_cost_price'), output_field=FloatField()))

            total_of_total_cost_price = total_of_total_cost_price['total_cost_price']

            self.profit = self.total_of_total_selling_price - total_of_total_cost_price
            print(self.profit)






            
        return self.filter_queryset(queryset)

    def perform_create(self, serializer):
        """
        Associate the current user with the created sale.
        """
        author = serializer.validated_data.get('author', None)
        if author is None:
            author = self.request.user
        serializer.save(author=author)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = OrderedDict([
                ('count', self.paginator.page.paginator.count),
                ('next', self.paginator.page.next_page_number() if self.paginator.page.has_next() else None),
                ('previous', self.paginator.page.previous_page_number() if self.paginator.page.has_previous() else None),
            ])
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = OrderedDict([
                ('count', queryset.count()),
                ('next', None),
                ('previous', None),
            ])

        if 'article_id' in self.request.GET:
            data['total_of_total_selling_price'] = self.total_of_total_selling_price
            data['profit'] = self.profit

        data['results'] = serializer.data

        return Response(data)