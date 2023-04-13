from django.urls import reverse_lazy, reverse
from django.forms.models import model_to_dict
from users.models import User
from sales.models import ArticleCategory, Article, Sale
from rest_framework.test import APITestCase
from rest_framework import status


class TestArticle(APITestCase):

    url = reverse_lazy('article-list')

    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

    def test_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access the Article API GET endpoint.
        """

        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)    

    def test_list_authenticated(self):
        """
        Test that authenticated users can't access the Article GET API endpoint.
        """

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN )

    def test_create_article(self):
        """
        Test that an authenticated user can create a new article.
        """

        category = ArticleCategory.objects.create(id=1, display_name='Category')

        article_data = {
            'code': 'ABC124',
            'category': category.id,
            'name': 'Test Article',
            'manufacturing_cost': 10.00
        }

        response = self.client.post(self.url, data=article_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.first().name, 'Test Article')

    def test_create_article_unauthenticated(self):
        """
        Test that an unauthenticated user can't create a new article.
        """
        self.client.force_authenticate(user=None)

        article_data = {
            'code': 'ABC125',
            'category': 1,
            'name': 'Test Article',
            'manufacturing_cost': 10.00
        }

        response = self.client.post(self.url, data=article_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Article.objects.count(), 0)


class TestSale(APITestCase):

    url = reverse_lazy('sale-list')

    def setUp(self):

        # Create a user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        # Create an article to be used for creating the sale
        self.article = Article.objects.create(
            code='ABC123',
            category=ArticleCategory.objects.create(display_name='Category'),
            name='Test Article',
            manufacturing_cost=10.00
        )

        self.sale_to_update = Sale.objects.create(
            date='2023-04-09',
            author=self.user,
            article=self.article,
            quantity=5,
            unit_selling_price=25.00
        )

        # Create a sale to be used for testing deletion
        self.sale_to_delete = Sale.objects.create(
            date='2023-04-09',
            author=self.user,
            article=self.article,
            quantity=5,
            unit_selling_price=25.00
        )

    def test_create_sale(self):
        """
        Test that an authenticated user can create a new sale.
        """
        sale_data = {
            'date': '2023-04-09',
            'author': self.user.id,
            'article': self.article.id,
            'quantity': 5,
            'unit_selling_price': 25.00
        }

        response = self.client.post(self.url, data=sale_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sale.objects.count(), 3)
        self.assertEqual(Sale.objects.first().author, self.user)

    def test_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access the Sale API GET endpoint.
        """
        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_authenticated(self):
        """
        Test that authenticated users can access the Sale API GET endpoint.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_sale_by_author(self):
        """
        Test that the author of a sale can update it using the PUT method.
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.put(
            reverse('sale-detail', args=[self.sale_to_update.id]),
            {
                'date': self.sale_to_update.date,
                'author': self.sale_to_update.author.id,
                'article': self.sale_to_update.article.id,
                'unit_selling_price': self.sale_to_update.unit_selling_price,
                'quantity': 10
            }
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 10)


    def test_delete_sale_author(self):
        """
        Test that the author of a sale can delete it.
        """
        self.client.force_authenticate(user=self.user)
        print(self.sale_to_delete.id)
        response = self.client.delete(reverse('sale-detail', args=[self.sale_to_delete.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_sale_not_author(self):
        """
        Test that a user who is not the author of a sale can't delete it.
        """
        other_user = User.objects.create_user(
            email='otheruser@example.com',
            password='testpass'
        )
        self.client.force_authenticate(user=other_user)
        response = self.client.delete(reverse('sale-detail', args=[self.sale_to_delete.id]))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)