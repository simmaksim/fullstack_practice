import uuid
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404


class UserManager(BaseUserManager):
    def get_object_by_public_id(self, public_id):
        try:
            return self.get(public_id=public_id)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404

    def create_user(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError("No username")
        if email is None:
            raise TypeError("No email")
        if password is None:
            raise TypeError("No password")
        item = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        item.set_password(password)
        item.save(using=self._db)
        return item

    def create_superuser(self, username, email, password=None, **kwargs):
        if username is None:
            raise TypeError("No username")
        if email is None:
            raise TypeError("No email")
        if password is None:
            raise TypeError("No password")
        item = self.create_user(
            username=username, email=email, password=password, **kwargs
        )
        item.is_superuser = True
        item.is_staff = True
        item.save(using=self._db)
        return item


class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()

    def __str__(self):
        return f"{self.email}"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


