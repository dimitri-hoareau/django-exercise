from collections import OrderedDict
from django.db.models import F, FloatField, Sum
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from sales.models import Article, Sale
from sales.serializers import ArticleSerializer, SaleSerializer
from .permissions import CreateOnly, IsOwnerOrReadOnly
 
class ArticleViewset(ModelViewSet):
    """
    Viewset for the Article model
    """

    permission_classes = [IsAuthenticated, CreateOnly]
 
    serializer_class = ArticleSerializer
 
    def get_queryset(self):
        return Article.objects.all()


class SaleViewset(ModelViewSet):
    """
    Viewset for the Sale model
    """
    
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

            self.last_selling_date = queryset.order_by('-date').first().date

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
            total_of_total_cost_price = queryset.annotate(
                total_cost_price=F('quantity') * F('article__manufacturing_cost')
            )

            total_of_total_cost_price = total_of_total_cost_price.aggregate(total_cost_price=Sum(F('total_cost_price'), output_field=FloatField()))

            total_of_total_cost_price = total_of_total_cost_price['total_cost_price']

            self.profit = self.total_of_total_selling_price - total_of_total_cost_price

            # Get the last selling date
            self.last_selling_date = queryset.order_by('-date').first().date

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
            data['last_selling_date'] = self.last_selling_date

        data['results'] = serializer.data

        return Response(data)