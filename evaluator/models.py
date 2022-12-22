from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel, Category


class Evaluator(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = "evaluators"
        verbose_name = "Evaluador"
        verbose_name_plural = "Evaluadores"
