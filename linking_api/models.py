from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=200, unique=True)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    # Establece is_active en True por defecto para todos los usuarios
    is_active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, related_name="custom_user_set", blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name="custom_user_set", blank=True
    )


class Link(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)