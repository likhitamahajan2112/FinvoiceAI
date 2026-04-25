from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, account_number, password=None, **extra_fields):
        if not account_number:
            raise ValueError("The Account Number must be set")
        user = self.model(account_number=account_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, account_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(account_number, password, **extra_fields)


class User(AbstractUser):
    username = None  # remove the default username field
    account_number = models.CharField(max_length=20, unique=True)
    pin = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    USERNAME_FIELD = 'account_number'
    REQUIRED_FIELDS = []  # removes email requirement

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.account_number} (Balance: ₹{self.balance})"


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=10,
        choices=[('credit', 'Credit'), ('debit', 'Debit')]
    )
    description = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.account_number} - {self.type} ₹{self.amount}"