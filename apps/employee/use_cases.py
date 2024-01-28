from apps.employee.models import Employee


class AllEmployeeListUseCase:
    def __init__(self, company_id):
        self._company_id = company_id

    def execute(self):
        return self._factory()

    def _factory(self):
        if self._company_id:
            self._employees = Employee.objects.filter(company_id=self._company_id).order_by('-created_at')
        else:
            self._devices = Employee.objects.all().order_by('-created_at')
        return self._employees
