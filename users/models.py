from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# ---------------------------
# 使用者管理器
# ---------------------------
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# ---------------------------
# 使用者主模型
# ---------------------------
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # 可登入 admin site
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

# ---------------------------
# 一般會員（消費者）
# ---------------------------
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    birthday = models.DateField(null=True, blank=True)
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def membership_level(self):
        if self.total_spent >= 10000:
            return "VIP"
        elif self.total_spent >= 5000:
            return "Gold"
        elif self.total_spent >= 1000:
            return "Silver"
        else:
            return "Basic"

    def __str__(self):
        return f"{self.full_name} ({self.user.email})"

# ---------------------------
# 商家 / 管理員
# ---------------------------
class AdminUser(models.Model):
    ROLE_CHOICES = (
        ('merchant', '商家'),
        ('manager', '網站管理員'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    display_name = models.CharField(max_length=100)
    brand_name = models.CharField(max_length=100, blank=True, null=True)
    brand_logo = models.ImageField(upload_to='brand_logos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.display_name} ({self.get_role_display()})"
