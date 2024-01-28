from django.contrib import admin

from apps.payment.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'amount',
        'payment_date',
        'payment_method',
        'user',
        'transaction_id',
        'description',
        'status',
        'company',
        'created_at',
        'updated_at',
    ]
    search_fields = (
        'id', 'amount', 'payment_date', 'payment_method', 'user', 'transaction_id', 'description', 'status',
        'company', 'created_at', 'updated_at')
    ordering = ('-created_at',)
