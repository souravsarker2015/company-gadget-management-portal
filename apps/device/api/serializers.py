from rest_framework import serializers

from apps.device.models import Device, DeviceLog


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        # fields = "__all__"
        exclude = ("company",)


class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog
        # fields = "__all__"
        exclude = ("company",)
