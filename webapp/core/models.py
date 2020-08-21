from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Entity(models.Model):
    """Abstract base models for all models in the application. Defines common attribute
    used in all models in the application.
    """
    id = models.BigAutoField(primary_key=True)

    class Meta:
        abstract = True


class Document(Entity):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='documents/')
    is_active = models.BooleanField('Is Active')

    def __str__(self):
        return f"{self.file.name}"


class Description(Entity):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    is_active = models.BooleanField('Is Active')

    def __str__(self):
        return f"{self.text[0:10]} ..."
