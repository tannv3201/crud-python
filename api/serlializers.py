from rest_framework import serializers

from .models import School, Student, Classroom


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name', 'address', 'createdAt', 'updatedAt')


class ClassroomSerializer(serializers.ModelSerializer):
    school = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = ('id', 'name', 'school_id', 'school', 'createdAt', 'updatedAt')

    def get_school(self, obj):
        has_school = self.context.get('has_school', False)
        if has_school:
            return SchoolSerializer(obj.school_id).data
        return None


class StudentSerializer(serializers.ModelSerializer):
    classroom = serializers.SerializerMethodField()
    school = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'name', 'classroom_id', 'classroom', 'school', 'createdAt', 'updatedAt')

    def get_classroom(self, obj):
        has_classroom = self.context.get('has_classroom', False)
        if has_classroom:
            return ClassroomSerializer(obj.classroom_id).data
        return None

    def get_school(self, obj):
        has_school = self.context.get('has_school', False)
        if has_school:
            classroom = obj.classroom_id
            return SchoolSerializer(classroom.school_id).data
        return None
