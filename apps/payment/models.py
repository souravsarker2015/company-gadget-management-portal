from django.db import models

from apps.company.models import Company
from apps.core.models import BaseModel
from apps.payment.utils import STATUS_CHOICES
from apps.users.models import User


class Payment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.user.name} - {self.amount} on {self.payment_date}"

    class Meta:
        db_table = 'payment'
