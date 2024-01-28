from django.contrib import admin

from apps.employee.models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email',
        'phone',
        'gender',
        'address',
        'date_of_birth',
        'employee_id',
        'position',
        'department',
        'hire_date',
        'salary',
        'company',
        'created_at',
        'updated_at',
    ]
    search_fields = (
        'id', 'name', 'email', 'phone', 'address', 'date_of_birth', 'employee_id', 'position',
        'department', 'hire_date', 'salary', 'company', 'created_at', 'updated_at')
    ordering = ('-created_at',)
