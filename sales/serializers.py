
from rest_framework.serializers import ModelSerializer, SerializerMethodField
 
from sales.models import Article, Sale
 
class ArticleSerializer(ModelSerializer):
    """
    Serializer for the Article model
    """
 
    class Meta:
        model = Article
        fields = ['id', 'code', 'category', 'name', 'manufacturing_cost']

class ArticleBasicSerializer(ModelSerializer):
    """
    Serializer for the Article model, including only the category and name fields,
    used into SaleSerializer
    """

    class Meta:
        model = Article
        fields = ['category', 'name']


class SaleSerializer(ModelSerializer):
    """
    Serializer for the Sale model
    """

    article = ArticleBasicSerializer()
    total_selling_price = SerializerMethodField()
 
    class Meta:
        model = Sale
        fields = ['id','date', 'author', 'article', 'quantity', 'unit_selling_price', 'total_selling_price']

    def get_total_selling_price(self, obj):
        return obj.quantity * obj.unit_selling_price
