import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models

from core.models import BaseModel
from evaluator.models import Evaluator


class Project(BaseModel):
    CREATED = "created"
    DRAFT = "draft"
    SEND = "send"
    FOR_CORRECTION = "for_correction"
    IN_CORRECTION = "in_correction"
    QUALIFIED = "qualified"

    STATUS = [
        (CREATED, "Creado"),
        (DRAFT, "Borrador"),
        (SEND, "Enviado"),
        (FOR_CORRECTION, "Para corrección"),
        (IN_CORRECTION, "En corrección"),
        (QUALIFIED, "Calificado"),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=STATUS, default=CREATED)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "projects"
        verbose_name = "Proyecto"
        verbose_name_plural = "Proyectos"


def path_and_rename(instance, filename):
    upload_to = 'uploads/projects'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class FilesApp(BaseModel):
    PDF = "pdf"
    PNG = "png"
    JPG = "jpg"
    JPEG = "jpeg"
    TYPE_ = [
        (PDF, "PDF"),
        (PNG, "PNG"),
        (JPG, "JPG"),
        (JPEG, "JPEG"),
    ]

    name = models.CharField(max_length=200)
    file = models.FileField(upload_to=path_and_rename)
    type_file = models.CharField(max_length=4, choices=TYPE_, default="")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "files"
        verbose_name = "Archivo"
        verbose_name_plural = "Archivos"


class Score(BaseModel):
    GENERAL = "general"
    FILES = "files"
    TYPE_EXTRA = [
        (GENERAL, "Descripción general"),
        (FILES, "Archivos"),
    ]

    score = models.DecimalField(max_digits=3, decimal_places=2)
    evaluator = models.ForeignKey(Evaluator, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    extra = models.CharField(max_length=10, choices=TYPE_EXTRA, default="", null=True, blank=True)

    class Meta:
        db_table = "scores"
        verbose_name = "Puntuación"
        verbose_name_plural = "Puntuaciones"
