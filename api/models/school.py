from django.db import models

from api.models.base import BaseUUIDModel


class School(BaseUUIDModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        db_table = "school"

    def __str__(self):
        return self.name
