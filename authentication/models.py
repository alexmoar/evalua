from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.contrib.auth.models import User

from core.models import BaseModel


class UserInformation(models.Model):
    ADMIN = "admin"
    EVALUATOR = "evaluator"
    WRITER = "writer"

    ROL = [
        (ADMIN, "Administrador"),
        (EVALUATOR, "Evaluador"),
        (WRITER, "Escritor"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    identification = models.CharField(
        "Identificación", max_length=255, blank=True, null=True
    )
    cellphone = models.CharField("Teléfono", max_length=255)
    biography = models.TextField("Biografía")
    photo = models.CharField("Foto", max_length=255)
    role = models.CharField(
        max_length=9,
        choices=ROL
    )
    show_intro = models.BooleanField(default=True)
    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return f"{self.id} | {self.user.first_name} {self.user.last_name}"

    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @property
    def get_role(self):
        return self.get_role_display()

    full_name.fget.short_description = "Nombre"
