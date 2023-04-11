
from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField
 
from sales.models import Article, Sale
from users.models import User
 
class ArticleSerializer(ModelSerializer):
    """
    Serializer for the Article model
    """
 
    class Meta:
        model = Article
        fields = ['id', 'code', 'category', 'name', 'manufacturing_cost']


class SaleSerializer(ModelSerializer):
    """
    Serializer for the Sale model
    """

    author = PrimaryKeyRelatedField(queryset=User.objects.all()) # This line add author selection in SaleSerializer
    article_category = SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'date', 'author', 'article', 'article_category', 'quantity', 'unit_selling_price', 'total_selling_price']

    def get_article_category(self, obj):
        return obj.article.category.display_name