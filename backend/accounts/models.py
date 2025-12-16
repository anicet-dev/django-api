from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(UserManager):
    pass

class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("user", "User"),
    )

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")

    # OTP
    phone_otp = models.CharField(max_length=6, blank=True, null=True)
    phone_otp_created = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return f"{self.email} ({self.role})"

    def set_otp(self, code, ttl_seconds=300):
        self.phone_otp = code
        self.phone_otp_created = timezone.now()
        self.save()

    def clear_otp(self):
        self.phone_otp = None
        self.phone_otp_created = None
        self.save()

    def otp_valid(self, code, ttl_seconds=300):
        if not (self.phone_otp and self.phone_otp_created):
            return False
        if self.phone_otp != code:
            return False
        if timezone.now() > self.phone_otp_created + timedelta(seconds=ttl_seconds):
            return False
        return True
