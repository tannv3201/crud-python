from rest_framework import serializers

from .models import Item, School, Student, ClassRoom


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('category', 'subcategory', 'name', 'amount')


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name', 'address')


class ClassRoomSerializer(serializers.ModelSerializer):
    school = serializers.SerializerMethodField()

    class Meta:
        model = ClassRoom
        fields = ('id', 'name', 'school', 'school_')

    def get_school_(self, obj):
        has_school = self.context.get('has_school', False)
        if has_school:
            return SchoolSerializer(obj.school_id).data
        return None


class StudentSerializer(serializers.ModelSerializer):
    class_ = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'name', 'class_room_id', 'class_')

    def get_class_(self, obj):
        has_class = self.context.get('has_class', False)
        if has_class:
            return ClassRoomSerializer(obj.class_room_id).data
        return None
