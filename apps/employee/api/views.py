from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from apps.company.utils import company_id_header_params
from apps.employee.api.serializers import EmployeeSerializer
from apps.employee.use_cases import AllEmployeeListUseCase
from rest_framework import serializers
from rest_framework import status


class EmployeeCreate(CreateAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllEmployeeListUseCase(company_id).execute()

    def perform_create(self, serializer):
        company_id = self.request.META.get('HTTP_COMPANY')
        print("company_id: ", company_id)
        if company_id is None:
            raise serializers.ValidationError({'error': 'Company ID not provided in the request header'})

        serializer.save(company_id=company_id)
        return Response(serializer.data)

    @swagger_auto_schema(tags=["Employee"], manual_parameters=company_id_header_params(),
                         request_body=EmployeeSerializer)
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class EmployeeListApiView(ListAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllEmployeeListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Employee"], manual_parameters=company_id_header_params())
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class EmployeeRetrieveAPIView(RetrieveAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllEmployeeListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Employee"], manual_parameters=company_id_header_params())
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class EmployeeUpdateApiView(UpdateAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllEmployeeListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Employee"], manual_parameters=company_id_header_params(),
                         request_body=EmployeeSerializer)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Employee"], manual_parameters=company_id_header_params(),
                         request_body=EmployeeSerializer)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class EmployeeDestroyAPIView(DestroyAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllEmployeeListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Employee"], manual_parameters=company_id_header_params(),
                         request_body=EmployeeSerializer)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
