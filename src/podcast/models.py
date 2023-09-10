from django.db import models

from main.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Owner(BaseModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return self.name
