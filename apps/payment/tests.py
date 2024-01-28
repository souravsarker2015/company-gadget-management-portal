from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from .api.serializers import PaymentSerializer
from .models import Payment
from ..company.models import Company
from ..users.models import User


class PaymentAPITest(APITestCase):
    def setUp(self):
        pass

    def test_serializer_valid(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        user = User.objects.create(name='Test User', email='test@example.com')
        data = {
            "user": user.id,
            "company": company.id,
        }

        serializer = PaymentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user.delete()
        company.delete()

    def test_create_payment(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        user = User.objects.create(name='Test User', email='test@example.com')
        data = {
            "company": company.id,
            "user": user.id,
        }
        response = self.client.post('/api/payment/create/', data, HTTP_COMPANY=str(company.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        payment = Payment.objects.get(user_id=user.id, company_id=company.id)
        self.assertIsNotNone(payment)
        self.assertEqual(payment.company.id, company.id)
        self.assertEqual(payment.user.id, user.id)

        user.delete()
        payment.delete()
        company.delete()

    def test_create_payment_missing_company_header(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        user = User.objects.create(name='Test User', email='test@example.com')

        data = {
            "company": company.id,
            "user": user.id,
        }
        response = self.client.post('/api/device/log/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_payment_list_api_view(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        user = User.objects.create(name='Test User', email='test@example.com')
        payment = Payment.objects.create(user_id=user.id, company_id=company.id)
        response = self.client.get('/api/payment/list/', HTTP_COMPANY=company.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Payment.objects.count())
        self.assertEqual(response.data[0]['user'], user.id)

        payment.delete()
        user.delete()
        company.delete()

    def test_retrieve_payment(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        user = User.objects.create(name='Test User', email='test@example.com')
        payment = Payment.objects.create(user_id=user.id, company_id=company.id)

        response = self.client.get(f'/api/payment/details/{payment.id}/', HTTP_COMPANY=company.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], user.id)
        payment.delete()
        user.delete()
        company.delete()

    def test_update_payment(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        user = User.objects.create(name='Test User', email='test@example.com')
        payment = Payment.objects.create(user_id=user.id, company_id=company.id)

        updated_data = {
            "description": "payment description",
        }
        response_put = self.client.put(
            f'/api/payment/update/{payment.id}/',
            data=updated_data,
            HTTP_COMPANY=company.id
        )
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        updated_payment = Payment.objects.get(id=payment.id)
        self.assertEqual(updated_payment.description, 'payment description')

        response_patch = self.client.patch(
            f'/api/payment/update/{payment.id}/',
            data=updated_data,
            HTTP_COMPANY=company.id
        )
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        patched_payment = Payment.objects.get(id=payment.id)
        self.assertEqual(patched_payment.description, 'payment description')
        payment.delete()
        user.delete()
        company.delete()

    def test_delete_device_log(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        user = User.objects.create(name='Test User', email='test@example.com')
        payment = Payment.objects.create(user_id=user.id, company_id=company.id)

        response = self.client.delete(f'/api/payment/delete/{payment.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Payment.DoesNotExist):
            Payment.objects.get(pk=payment.id)
