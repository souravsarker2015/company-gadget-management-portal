from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase
from .models import Device, DeviceLog
from .api.serializers import DeviceSerializer, DeviceLogSerializer
from ..company.models import Company
import uuid
from rest_framework.reverse import reverse

from ..employee.models import Employee


class DeviceAPITest(APITestCase):
    def setUp(self):
        pass

    def test_serializer_valid(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        data = {
            'name': 'Test Device',
            'description': 'Test description',
            'serial_number': '123456',
            'brand': 'TestBrand',
            'model_number': 'TestModel',
            'warranty_period_months': 12,
            'is_available': True,
            'purchase_date': '2022-01-28',
            'purchase_cost': 100.00,
            'last_maintenance_date': '2022-01-28',
            'company': company.id
        }

        serializer = DeviceSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        company.delete()

    def test_create_device(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        data = {
            'name': 'Test Device',
            'description': 'Device for testing',
            'serial_number': '123456',
            'brand': 'TestBrand',
            'model_number': 'TestModel',
            'warranty_period_months': 12,
            'is_available': True,
            'purchase_date': '2023-01-28',
            'purchase_cost': '500.00',
            'last_maintenance_date': '2023-01-28',
        }
        response = self.client.post('/api/device/create/', data, HTTP_COMPANY=str(company.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device = Device.objects.get(name='Test Device')
        self.assertIsNotNone(device)
        self.assertEqual(device.name, 'Test Device')
        self.assertEqual(device.description, 'Device for testing')
        device.delete()
        company.delete()

    def test_create_device_missing_company_header(self):
        data = {
            'name': 'Test Device',
            'description': 'Device for testing',
            'serial_number': '123456',
            'brand': 'TestBrand',
            'model_number': 'TestModel',
            'warranty_period_months': 12,
            'is_available': True,
            'purchase_date': '2023-01-28',
            'purchase_cost': '500.00',
            'last_maintenance_date': '2023-01-28',
        }
        response = self.client.post('/api/device/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_device_list_api_view(self):
        company = Company.objects.create(name='Existing Company', email='existing@example.com')
        device = Device.objects.create(name='Existing Device', company_id=company.id)
        response = self.client.get('/api/device/list/', {'HTTP_COMPANY': company.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Device.objects.count())
        self.assertEqual(response.data[0]['name'], 'Existing Device')
        device.delete()
        company.delete()

    def test_retrieve_device(self):
        company = Company.objects.create(name='Existing Company', email='existing@example.com')
        device = Device.objects.create(name='Existing Device', company_id=company.id)
        response = self.client.get(f'/api/device/details/{device.id}/', {'HTTP_COMPANY': company.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Existing Device')
        device.delete()
        company.delete()

    def test_update_device(self):
        company = Company.objects.create(name='Existing Company', email='existing@example.com')
        device = Device.objects.create(name='Existing Device', company_id=company.id)
        updated_data = {
            'name': 'Existing Device',
        }
        response_put = self.client.put(
            f'/api/device/update/{device.id}/',
            data=updated_data,
            HTTP_COMPANY=company.id
        )
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        updated_device = Device.objects.get(id=device.id)
        self.assertEqual(updated_device.name, 'Existing Device')
        response_patch = self.client.patch(
            f'/api/device/update/{device.id}/',
            data=updated_data,
            HTTP_COMPANY=company.id
        )
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        patched_device = Device.objects.get(id=device.id)
        self.assertEqual(patched_device.name, 'Existing Device')
        company.delete()
        device.delete()

    def test_delete_device(self):
        company = Company.objects.create(name='Existing Company', email='existing@example.com')
        device = Device.objects.create(name='Existing Device', company_id=company.id)

        response = self.client.delete(f'/api/device/delete/{device.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Device.DoesNotExist):
            Device.objects.get(pk=device.id)


class DeviceLogAPITest(APITestCase):
    def setUp(self):
        pass

    def test_serializer_valid(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)
        device = Device.objects.create(name='Existing Device', company_id=company.id)
        data = {
            "is_returned": False,
            "device": device.id,
            "employee": employee.id,
        }

        serializer = DeviceLogSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        employee.delete()
        device.delete()
        company.delete()

    def test_create_device_log(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)
        device = Device.objects.create(name='Existing Device', company_id=company.id)

        data = {
            "is_returned": False,
            "device": device.id,
            "employee": employee.id,
        }
        response = self.client.post('/api/device/log/create/', data, HTTP_COMPANY=str(company.id))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        device_log = DeviceLog.objects.get(device_id=device.id, employee_id=employee.id)
        self.assertIsNotNone(device_log)
        self.assertEqual(device_log.employee.id, employee.id)
        self.assertEqual(device_log.device.id, device.id)
        device_log.delete()
        device.delete()
        employee.delete()
        company.delete()

    def test_create_device_log_missing_company_header(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)
        device = Device.objects.create(name='Existing Device', company_id=company.id)

        data = {
            "is_returned": False,
            "device": device.id,
            "employee": employee.id,
        }
        response = self.client.post('/api/device/log/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_device_log_list_api_view(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)
        device = Device.objects.create(name='Existing Device', company_id=company.id)
        device_log = DeviceLog.objects.create(company_id=company.id, device_id=device.id, employee_id=employee.id)
        response = self.client.get('/api/device/log/list/', {'HTTP_COMPANY': company.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), DeviceLog.objects.count())
        self.assertEqual(response.data[0]['employee'], employee.id)

        device_log.delete()
        device.delete()
        employee.delete()
        company.delete()

    def test_retrieve_device_log(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)
        device = Device.objects.create(name='Existing Device', company_id=company.id)
        device_log = DeviceLog.objects.create(company_id=company.id, device_id=device.id, employee_id=employee.id)

        response = self.client.get(f'/api/device/log/details/{device_log.id}/', {'HTTP_COMPANY': company.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['employee'], employee.id)
        device_log.delete()
        device.delete()
        employee.delete()
        company.delete()

    def test_update_device_log(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)
        device = Device.objects.create(name='Existing Device', company_id=company.id)
        device_log = DeviceLog.objects.create(company_id=company.id, device_id=device.id, employee_id=employee.id)

        updated_data = {
            "assign_time_condition": "good",
        }
        response_put = self.client.put(
            f'/api/device/log/update/{device_log.id}/',
            data=updated_data,
            HTTP_COMPANY=company.id
        )
        self.assertEqual(response_put.status_code, status.HTTP_200_OK)
        updated_device_log = DeviceLog.objects.get(id=device_log.id)
        self.assertEqual(updated_device_log.assign_time_condition, 'good')

        response_patch = self.client.patch(
            f'/api/device/log/update/{device_log.id}/',
            data=updated_data,
            HTTP_COMPANY=company.id
        )
        self.assertEqual(response_patch.status_code, status.HTTP_200_OK)
        patched_device_log = DeviceLog.objects.get(id=device_log.id)
        self.assertEqual(patched_device_log.assign_time_condition, 'good')
        device_log.delete()
        device.delete()
        employee.delete()
        company.delete()

    def test_delete_device_log(self):
        company = Company.objects.create(name='Test Company', email='test@example.com')
        employee = Employee.objects.create(name='Existing Employee', company_id=company.id)
        device = Device.objects.create(name='Existing Device', company_id=company.id)
        device_log = DeviceLog.objects.create(company_id=company.id, device_id=device.id, employee_id=employee.id)

        response = self.client.delete(f'/api/device/log/delete/{device_log.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(DeviceLog.DoesNotExist):
            DeviceLog.objects.get(pk=device_log.id)
