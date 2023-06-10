from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.db import models
from django.db.models import TextChoices

from users.managers import UserManager


class UserRoles(TextChoices):
    USER = "user", "Пользователь"
    ADMIN = "admin", "Администратор"


class User(AbstractBaseUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['first_name', 'last_name', 'phone', 'role']

    objects = UserManager()

    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=6, choices=UserRoles.choices, default=UserRoles.USER)
    image = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_active = models.BooleanField()

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self):
        return self.is_admin

    def has_module_perm(self):
        return self.is_admin

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_user(self):
        return self.role == UserRoles.USER

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
