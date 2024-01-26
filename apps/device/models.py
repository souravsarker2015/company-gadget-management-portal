from django.db import models

from apps.core.models import BaseModel
from apps.employee.models import Employee


class Device(BaseModel):
    name = models.CharField(max_length=254)
    description = models.TextField(null=True, blank=True)
    serial_number = models.CharField(max_length=254, null=True, blank=True)
    brand = models.CharField(max_length=254, null=True, blank=True)
    model_number = models.CharField(max_length=254, null=True, blank=True)
    warranty_period_months = models.PositiveIntegerField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    purchase_date = models.DateField(null=True, blank=True)
    purchase_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_maintenance_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'device'


class DeviceLog(BaseModel):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True, blank=True)
    assign_date = models.DateField(null=True, blank=True)
    assign_time_condition = models.TextField(blank=True, null=True)
    return_date = models.DateField(null=True, blank=True)
    return_time_condition = models.TextField(blank=True, null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.device.name

    class Meta:
        db_table = 'device_log'
