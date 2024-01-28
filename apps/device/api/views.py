from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.response import Response

from apps.company.utils import company_id_header_params
from apps.device.api.serializers import DeviceSerializer, DeviceLogSerializer
from apps.device.use_cases import AllDeviceListUseCase, AllDeviceLogListUseCase, DeviceUpdateUseCase
from rest_framework import serializers

from rest_framework import status
from rest_framework.response import Response


class DeviceCreate(CreateAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllDeviceListUseCase(company_id).execute()

    def perform_create(self, serializer):
        company_id = self.request.META.get('HTTP_COMPANY')
        print("company_id: ", company_id)
        if company_id is None:
            raise serializers.ValidationError({'error': 'Company ID not provided in the request header'})

        serializer.save(company_id=company_id)
        return Response(serializer.data)

    @swagger_auto_schema(tags=["Device"], manual_parameters=company_id_header_params(), request_body=DeviceSerializer)
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class DeviceListApiView(ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        print('device company id: ', company_id)
        return AllDeviceListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Device"], manual_parameters=company_id_header_params())
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DeviceRetrieveAPIView(RetrieveAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllDeviceListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Device"], manual_parameters=company_id_header_params())
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DeviceUpdateApiView(UpdateAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllDeviceListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Device"], manual_parameters=company_id_header_params(), request_body=DeviceSerializer)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Device"], manual_parameters=company_id_header_params(), request_body=DeviceSerializer)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DeviceDestroyAPIView(DestroyAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllDeviceListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Device"], manual_parameters=company_id_header_params(), request_body=DeviceSerializer)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DeviceLogCreate(CreateAPIView):
    serializer_class = DeviceLogSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllDeviceLogListUseCase(company_id).execute()

    def perform_create(self, serializer):
        company_id = self.request.META.get('HTTP_COMPANY')
        if company_id is None:
            raise serializers.ValidationError({'error': 'Company ID not provided in the request header'})

        device_log = serializer.save(company_id=company_id)
        DeviceUpdateUseCase(device_log.device, {"is_available": False}).execute()
        return Response(serializer.data)

    @swagger_auto_schema(tags=["Device Log"], manual_parameters=company_id_header_params(),
                         request_body=DeviceLogSerializer)
    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except serializers.ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)


class DeviceLogListApiView(ListAPIView):
    serializer_class = DeviceLogSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllDeviceLogListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Device"], manual_parameters=company_id_header_params())
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DeviceLogRetrieveAPIView(RetrieveAPIView):
    serializer_class = DeviceLogSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllDeviceLogListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Device"], manual_parameters=company_id_header_params())
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class DeviceLogUpdateApiView(UpdateAPIView):
    serializer_class = DeviceLogSerializer

    def perform_update(self, serializer):
        device_log = serializer.save()
        if device_log.is_returned:
            DeviceUpdateUseCase(device_log.device, {"is_available": True}).execute()
        return Response(serializer.data)

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllDeviceLogListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Device Log"], manual_parameters=company_id_header_params(),
                         request_body=DeviceLogSerializer)
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Device Log"], manual_parameters=company_id_header_params(),
                         request_body=DeviceSerializer)
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class DeviceLogDestroyAPIView(DestroyAPIView):
    serializer_class = DeviceLogSerializer

    def get_queryset(self):
        company_id = self.request.META.get('HTTP_COMPANY')
        return AllDeviceLogListUseCase(company_id).execute()

    @swagger_auto_schema(tags=["Device Log"], manual_parameters=company_id_header_params(),
                         request_body=DeviceLogSerializer)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
