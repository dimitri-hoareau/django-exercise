from django.urls import reverse_lazy
from users.models import User
from rest_framework.test import APITestCase
from rest_framework import status


class TestArticle(APITestCase):

    url = reverse_lazy('article-list')

    def test_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access the Article API GET endpoint.
        """

        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_authenticated(self):
        """
        Test that authenticated users can't access the Article GET API endpoint.
        """

        self.user = User.objects.create_user(
        email='testuser@example.com',
        password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN )

    # TEST POST OK 
    # TEST PUT/DELETE PAS OK


class TestSale(APITestCase):

    url = reverse_lazy('sale-list')

    def test_list_unauthenticated(self):
        """
        Test that unauthenticated users can't access the Sale API GET endpoint.
        """

        self.client.force_authenticate(user=None)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_authenticated(self):
        """
        Test that authenticated users can access the Sale API GET endpoint.
        """

        self.user = User.objects.create_user(
        email='testuser@example.com',
        password='testpass'
        )
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK )

    # TEST POST OK 
    # TEST PUT/DELETE SEULEMENT AUTH