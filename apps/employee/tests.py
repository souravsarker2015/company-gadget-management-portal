from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from .api.serializers import EmployeeSerializer
from .models import Employee
from ..company.models import Company
import uuid


class EmployeeAPITest(APITestCase):
    def setUp(self):
        pass

    def test_serializer_valid(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')

        data = {
            'name': 'Test Employee',
            'company': company.id
        }

        serializer = EmployeeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        company.delete()

    def test_create_employee(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')

        data = {
            'name': 'Test Employee',
        }
        response = self.client.post('/api/employee/create/', data, HTTP_COMPANY=str(company.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee = Employee.objects.get(name='Test Employee')
        self.assertIsNotNone(employee)
        self.assertEqual(employee.name, 'Test Employee')
        employee.delete()
        company.delete()

    def test_create_employee_missing_company_header(self):
        data = {
            'name': 'Test Employee',
        }
        response = self.client.post('/api/device/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_employee_list_api_view(self):
        company = Company.objects.create(name='Existing Company', email='existing@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)

        response = self.client.get('/api/employee/list/', HTTP_COMPANY=company.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Employee.objects.count())
        self.assertEqual(response.data[0]['name'], 'Existing Employee')
        employee.delete()
        company.delete()

    def test_retrieve_employee(self):
        company = Company.objects.create(name='Existing Company', email='existing@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)
        response = self.client.get(f'/api/employee/details/{employee.id}/', {'HTTP_COMPANY': company.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Existing Employee')
        employee.delete()
        company.delete()

    def test_update_employee(self):
        company = Company.objects.create(name='Existing Company', email='existing@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)
        updated_data = {
            'name': 'Existing Employee Up',
        }
        response_put = self.client.put(
            f'/api/employee/update/{employee.id}/',
            data=updated_data,
            HTTP_COMPANY=company.id
        )
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        updated_employee = Employee.objects.get(id=employee.id)
        self.assertEqual(updated_employee.name, 'Existing Employee Up')
        response_patch = self.client.patch(
            f'/api/employee/update/{employee.id}/',
            data=updated_data,
            HTTP_COMPANY=company.id
        )
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        patched_employee = Employee.objects.get(id=employee.id)
        self.assertEqual(patched_employee.name, 'Existing Employee Up')
        company.delete()
        employee.delete()

    def test_delete_employee(self):
        company = Company.objects.create(name='Existing Company', email='existing@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)

        response = self.client.delete(f'/api/employee/delete/{employee.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Employee.DoesNotExist):
            Employee.objects.get(pk=employee.id)
