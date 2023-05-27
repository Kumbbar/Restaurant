from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserTests(APITestCase):
    def test_create_user_bad_name(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register')
        data = {'username': 'test', 'password': 'Good34!pass4'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_bad_password(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register')
        data = {'username': 'interesting_name8', 'password': 'badpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_good_data(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register')
        data = {'username': 'interesting_name8', 'password': 'GooDPa33W*'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
