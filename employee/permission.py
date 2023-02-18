from django.contrib.auth.mixins import UserPassesTestMixin

class EmployeePassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_employee