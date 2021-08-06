from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email is a required field")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    # super user
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    # default attribute to login: Use the email as unique username
    USERNAME_FIELD = "email"

    email = models.EmailField(
        max_length=255,
        verbose_name="email address",
        db_index=True,
        help_text="Enter email address",
        unique=True,
        error_messages={
            "unique": "A user is already registered with this email address",
        },
    )

    is_verified = models.BooleanField(default=False)

    is_staff = models.BooleanField(
        verbose_name="staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_active = models.BooleanField(
        verbose_name="active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    # initial time user object is created
    created_at = models.DateTimeField(auto_now_add=True)
    # time the user object is updated
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    # def tokens(self):
    #     refresh = RefreshToken.for_user(self)
    #     return {"refresh": str(refresh), "access": str(refresh.access_token)}

    objects = UserManager()
