from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from .models import Company
from .api.serializers import CompanySerializer
from rest_framework.reverse import reverse


class CompanyAPITest(APITestCase):
    def setUp(self):
        pass

    def test_serializer_valid(self):
        data = {'name': 'Test Serializer', 'email': 'test@example.com'}
        serializer = CompanySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid(self):
        data = {'name': 'Test Serializer'}
        serializer = CompanySerializer(data=data)
        self.assertFalse(serializer.is_valid())

        data = {'name': 'Test Serializer', 'email': 'invalid_email'}
        serializer = CompanySerializer(data=data)
        self.assertFalse(serializer.is_valid())

    def test_create_company(self):
        data = {
            'name': 'Test Company',
            'email': 'test@example.com',
            'phone': '1234567890',
            'address': 'Test Address',
        }

        response = self.client.post('/api/company/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        company = Company.objects.get(name='Test Company')
        self.assertIsNotNone(company)
        self.assertEqual(response.data['name'], 'Test Company')
        company.delete()

    def test_list_view(self):
        company = Company.objects.create(name='Existing Company', email='existing@example.com')
        response = self.client.get('/api/company/list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Company.objects.count())
        self.assertEqual(response.data[0]['name'], 'Existing Company')
        company.delete()

    def test_retrieve_company(self):
        company = Company.objects.create(name='Retrieve Company', email='retrieve@example.com', phone='1234567890',
                                         address='Retrieve Address')

        response = self.client.get(reverse('company_details', kwargs={'pk': company.id}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data['name'], 'Retrieve Company')
        self.assertEqual(response.data['email'], 'retrieve@example.com')
        self.assertEqual(response.data['phone'], '1234567890')
        self.assertEqual(response.data['address'], 'Retrieve Address')

        company.delete()

    def test_update_company(self):
        company = Company.objects.create(name='Update Company', email='update@example.com', phone='1234567890',
                                         address='Update Address')

        updated_data = {
            'name': 'Updated Company',
            'email': 'updated@example.com',
            'phone': '9876543210',
            'address': 'Updated Address',
        }

        response_put = self.client.put(reverse('company_update', kwargs={'pk': company.id}), data=updated_data)
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        updated_company = Company.objects.get(id=company.id)

        self.assertEqual(updated_company.name, 'Updated Company')
        self.assertEqual(updated_company.email, 'updated@example.com')
        self.assertEqual(updated_company.phone, '9876543210')
        self.assertEqual(updated_company.address, 'Updated Address')

        response_patch = self.client.patch(reverse('company_update', kwargs={'pk': company.id}),
                                           data={'name': 'Patched Company'})

        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        patched_company = Company.objects.get(id=company.id)
        self.assertEqual(patched_company.name, 'Patched Company')
        company.delete()

    def test_delete_company(self):
        company = Company.objects.create(name='CompanyToDelete', email='delete@example.com')
        company_id = company.id
        response = self.client.delete(f'/api/company/delete/{company_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Company.DoesNotExist):
            Company.objects.get(pk=company_id)
