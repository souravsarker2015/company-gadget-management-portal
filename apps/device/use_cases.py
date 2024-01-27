from apps.device.models import Device, DeviceLog


class AllDeviceListUseCase:
    def __init__(self, company_id):
        self._company_id = company_id

    def execute(self):
        return self._factory()

    def _factory(self):
        if self._company_id:
            self._devices = Device.objects.filter(company_id=self._company_id).order_by('-created_at')
        else:
            self._devices = Device.objects.all().order_by('-created_at')
        return self._devices


class DeviceUpdateUseCase:
    def __init__(self, device_instance, update_data):
        self._device_instance = device_instance
        self._update_data = update_data

    def execute(self):
        return self._update_device()

    def _update_device(self):
        if self._device_instance:
            for key, value in self._update_data.items():
                setattr(self._device_instance, key, value)
            self._device_instance.save()
            return self._device_instance
        else:
            return None


class AllDeviceLogListUseCase:
    def __init__(self, company_id):
        self._company_id = company_id

    def execute(self):
        return self._factory()

    def _factory(self):
        if self._company_id:
            self._devices = DeviceLog.objects.filter(company_id=self._company_id).order_by('-created_at')
        else:
            self._devices = DeviceLog.objects.all().order_by('-created_at')
        return self._devices
