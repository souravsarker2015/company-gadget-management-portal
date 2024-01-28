from rest_framework import serializers

from apps.device.models import Device, DeviceLog


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        exclude = ("company",)


class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog
        exclude = ("company",)
