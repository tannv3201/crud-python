from uuid import uuid4

from django.db import models


class Item(models.Model):
    category = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    amount = models.PositiveIntegerField()

    class Meta:
        db_table = "item_test"

    def __str__(self) -> str:
        return self.name


class School(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    class Meta:
        db_table = "school"

    def __str__(self) -> str:
        return self.name


class ClassRoom(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='tb_class')

    class Meta:
        db_table = "class_room"

    def __str__(self) -> str:
        return self.name


class Student(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, related_name='tb_student', null=True,
                                   blank=True)

    class Meta:
        db_table = "student"

    def __str__(self) -> str:
        return self.name
