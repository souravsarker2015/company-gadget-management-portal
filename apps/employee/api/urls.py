from django.urls import path

from apps.employee.api import views

urlpatterns = [
    path('create/', views.EmployeeCreate.as_view(), name='employee_create'),
    path('list/', views.EmployeeListApiView.as_view(), name='employee_list'),
    path('details/<uuid:pk>/', views.EmployeeRetrieveAPIView.as_view(), name='employee_details'),
    path('update/<uuid:pk>/', views.EmployeeUpdateApiView.as_view(), name='employee_update'),
    path('delete/<uuid:pk>/', views.EmployeeDestroyAPIView.as_view(), name='employee_delete'),

]
