from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from .api.serializers import RegistrationSerializer, CustomLoginSerializer
from .models import User
from ..company.models import Company


class UserAPITest(APITestCase):
    def setUp(self):
        pass

    def test_registration_serializer_valid(self):
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'admin',
            'password2': 'admin',
        }

        serializer = RegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_login_serializer_valid(self):
        data = {
            'username': 'test@example.com',
            'password': 'admin',
        }

        serializer = CustomLoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_user_registration(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')

        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'admin',
            'password2': 'admin',
        }

        response = self.client.post('/user/register/', data, format='json', HTTP_COMPANY=str(company.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        company.delete()

    def test_user_login(self):
        company = Company.objects.create(name='Test Company', email='test1@example.com')
        user = User.objects.create(name='Test User', email='test@example.com', company_id=company.id)
        user.set_password('example')
        user.save()

        data = {
            'username': 'test@example.com',
            'password': 'example',
        }

        response = self.client.post('/user/login/', data, format='json', HTTP_COMPANY=str(company.id))
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        company.delete()
        user.delete()
