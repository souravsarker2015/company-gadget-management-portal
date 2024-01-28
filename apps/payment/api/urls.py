from django.urls import path

from apps.payment.api import views

urlpatterns = [
    path('create/', views.PaymentCreate.as_view(), name='payment_create'),
    path('list/', views.PaymentListApiView.as_view(), name='payment_list'),
    path('details/<uuid:pk>/', views.PaymentRetrieveAPIView.as_view(), name='payment_details'),
    path('update/<uuid:pk>/', views.PaymentUpdateApiView.as_view(), name='payment_update'),
    path('delete/<uuid:pk>/', views.PaymentDestroyAPIView.as_view(), name='payment_delete'),
]
