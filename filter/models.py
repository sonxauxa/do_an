from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class FileFormUpLoad(models.Model):
    file = models.FileField(upload_to='document/')
    owner = models.CharField(max_length=100, default="un know")

    def __str__(self):
        return self.file.name


class Files(models.Model):
    filename = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='store/pdfs/')
    cover = models.ImageField(upload_to='store/covers/', null=True, blank=True)

    def __str__(self):
        return self.filename

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)


class Pelcon(models.Model):
    name = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='store/pdfs/')

    def __str__(self):
        return self.name
