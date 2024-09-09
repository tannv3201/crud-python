from django.db import models

from api.models.base import BaseUUIDModel
from api.models.classroom import Classroom
from api.models.school import School


class Student(BaseUUIDModel):
    name = models.CharField(max_length=255)
    classroom_id = models.ForeignKey(Classroom, on_delete=models.SET_NULL, related_name='students', null=True,
                                     blank=True, db_column='classroom_id')
    school_id = models.ForeignKey(School, on_delete=models.SET_NULL, related_name='students', null=True,
                                  blank=True, db_column='school_id')

    class Meta:
        db_table = "student"

    def __str__(self):
        return self.name
