from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Roles(models.TextChoices):
        REGULAR = 'regular', 'Regular'
        STAFF = 'staff', 'Staff'
        ADMIN = 'admin', 'Admin'
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.REGULAR)
    bio = models.CharField(max_length=300, blank=True)

    def is_staffish(self) -> bool:
        return self.is_staff or self.role in {self.Roles.STAFF, self.Roles.ADMIN}
