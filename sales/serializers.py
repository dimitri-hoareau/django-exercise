from rest_framework.serializers import ModelSerializer
 
from sales.models import Article, Sale
 
class ArticleSerializer(ModelSerializer):
    """
    Serializer for the Article model
    """
 
    class Meta:
        model = Article
        fields = ['id', 'code', 'category', 'name', 'manufacturing_cost']