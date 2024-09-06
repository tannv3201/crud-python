from uuid import uuid4

from django.db import models


class BaseUUIDModel(models.Model):
    """Abstract base model with UUID primary key."""
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Item(models.Model):
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()

    class Meta:
        db_table = "item_test"

    def __str__(self):
        return self.name


class School(BaseUUIDModel):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        db_table = "school"

    def __str__(self):
        return self.name


class Classroom(BaseUUIDModel):
    name = models.CharField(max_length=255)
    school_id = models.ForeignKey(School, on_delete=models.CASCADE, related_name='classrooms', db_column='school_id')

    class Meta:
        db_table = "classroom"

    def __str__(self):
        return self.name


class Student(BaseUUIDModel):
    name = models.CharField(max_length=255)
    classroom_id = models.ForeignKey(Classroom, on_delete=models.SET_NULL, related_name='students', null=True,
                                     blank=True, db_column='classroom_id')

    class Meta:
        db_table = "student"

    def __str__(self):
        return self.name
