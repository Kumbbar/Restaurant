import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", ".settings")
django.setup()




import sys

project = os.path.dirname(os.path.abspath('manage.py'))
sys.path.append(project)
os.environ["DJANGO_SETTINGS_MODULE"] = "/mnt/c/Pycharm_Projects/Django/restaurant/auth/auth/settings.py"


from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AccountTests(APITestCase):
    def test_create_account(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('register')
        data = {'username': 'test', 'password': 'Good34!pass4'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
