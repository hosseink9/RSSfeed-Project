from django.db import models

from main.models import BaseModel

class Author(BaseModel):
    name = models.CharField(max_length=30)


    def __str__(self):
        return self.name