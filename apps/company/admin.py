
from django.contrib import admin

from apps.company.models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'name',
        'email',
        'phone',
        'address',
        'created_at',
        'updated_at',
    ]
    search_fields = ('id', 'name', 'email', 'phone', 'address', 'created_at', 'updated_at')
    ordering = ('-created_at',)
