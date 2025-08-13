from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class OwnerRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    owner_field = 'owner'

    def test_func(self):
        obj = self.get_object()
        return getattr(obj, self.owner_field) == self.request.user or self.request.user.is_staff
