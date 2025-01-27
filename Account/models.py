from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Username cannot be empty.')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('The superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('The superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)


class User(AbstractBaseUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="نام کاربری"
    )

    email = models.EmailField(
        unique=True,
        null=True,
        verbose_name='ایمیل'
    )

    phone = models.CharField(
        max_length=15,
        null=True,
        blank=True,
        verbose_name="شماره تلفن"
    )

    birthday = models.DateField(
        verbose_name="تاریخ تولد",
        null=True,
    )

    job = models.CharField(
        max_length=100,
        verbose_name="شغل",
        null=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="فعال"
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="کارمند"
    )

    is_superuser = models.BooleanField(
        default=False,
        verbose_name='ادمین',
    )

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


