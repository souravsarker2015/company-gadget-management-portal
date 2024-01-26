from apps.core.models import BaseModel
from django.db import models
from apps.employee.utils import GENDER_CHOICES


class Employee(BaseModel):
    name = models.CharField(max_length=254)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=254, null=True, blank=True)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES, blank=True, null=True)
    address = models.CharField(max_length=254, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    employee_id = models.CharField(max_length=20, unique=True)
    position = models.CharField(max_length=50, null=True, blank=True)
    department = models.CharField(max_length=50, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'employee'
