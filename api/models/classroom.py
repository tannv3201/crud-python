from django.db import models

from api.models.base import BaseUUIDModel
from api.models.school import School


class Classroom(BaseUUIDModel):
    name = models.CharField(max_length=255)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms', db_column='school_id')

    class Meta:
        db_table = "classroom"

    def __str__(self):
        return self.name
