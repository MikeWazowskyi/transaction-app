from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("The Email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    first_name = models.CharField("first name",
                                  max_length=150,
                                  blank=False)
    last_name = models.CharField("last name",
                                 max_length=150,
                                 blank=False)
    email = models.EmailField(unique=True)
    tax_id_number = models.CharField(
        validators=[
            RegexValidator(regex=r'^\d{12}$',
                           message='Tax id number has to be 12 digits',
                           code='nomatch')],
        max_length=12,
        unique=True,
        verbose_name='ИНН'
    )
    account = models.DecimalField(
        default=0.00,
        max_digits=20,
        decimal_places=2,
        verbose_name='Счет',
        validators=[MinValueValidator(0.00), ]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'first_name',
        'last_name',
        'tax_id_number',
    ]

    objects = CustomUserManager()

    class Meta:
        ordering = ['id', ]

    @property
    def full_name(self):
        return self.get_full_name()
