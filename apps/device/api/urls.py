from django.urls import path

from apps.device.api import views

urlpatterns = [
    path('create/', views.DeviceCreate.as_view(), name='device_create'),
    path('list/', views.DeviceListApiView.as_view(), name='device_list'),
    path('details/<uuid:pk>/', views.DeviceRetrieveAPIView.as_view(), name='device_details'),
    path('update/<uuid:pk>/', views.DeviceUpdateApiView.as_view(), name='device_update'),
    path('delete/<uuid:pk>/', views.DeviceDestroyAPIView.as_view(), name='company_delete'),

    path('log/create/', views.DeviceLogCreate.as_view(), name='device_log_create'),
    path('log/list/', views.DeviceLogListApiView.as_view(), name='device_log_list'),
    path('log/details/<uuid:pk>/', views.DeviceLogRetrieveAPIView.as_view(), name='device_log_details'),
    path('log/update/<uuid:pk>/', views.DeviceLogUpdateApiView.as_view(), name='device_log_update'),
    path('log/delete/<uuid:pk>/', views.DeviceLogDestroyAPIView.as_view(), name='company_log_delete'),
]
