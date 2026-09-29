from django.db import models

from django.contrib.auth.models import AbstractUser , BaseUserManager , PermissionsMixin

class CustomUserManager(BaseUserManager):
    def _create_user(self, phone, password='none', **extra_fields):
        if not phone:
            raise ValueError("phone must be set")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password='none', **extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password='none', **extra_fields):
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("is_staff for superuser must be True")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("is_superuser for superuser must be True")

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser, PermissionsMixin):
    phone = models.CharField(max_length=11, unique=True)
    first_name = models.CharField(max_length=100, blank=True, null= True)
    last_name = models.CharField(max_length=100, blank=True, null= True)
    date_of_birth = models.DateField(blank=True, null= True)
    is_active = models.BooleanField(default= True)
    is_staff = models.BooleanField(default= False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"