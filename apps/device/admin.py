from django.contrib import admin

from apps.device.models import Device, DeviceLog


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'description',
        'serial_number',
        'brand',
        'model_number',
        'warranty_period_months',
        'is_available',
        'purchase_date',
        'purchase_cost',
        'last_maintenance_date',
        'company',
        'created_at',
        'updated_at',
    ]
    search_fields = (
        'id', 'name', 'description', 'serial_number', 'brand', 'model_number', 'warranty_period_months', 'is_available',
        'purchase_date', 'purchase_cost', 'last_maintenance_date', 'company', 'created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(DeviceLog)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'device',
        'assign_date',
        'assign_time_condition',
        'is_returned',
        'return_date',
        'return_time_condition',
        'employee',
        'company',
        'created_at',
        'updated_at',
    ]
    search_fields = (
        'id', 'device', 'description', 'assign_date', 'assign_time_condition', 'is_returned', 'return_date',
        'return_time_condition', 'employee', 'company')
    ordering = ('-created_at',)
