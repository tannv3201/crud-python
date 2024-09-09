from rest_framework import serializers

from api.models.student import Student
from api.serializers.classroom import ClassroomSerializer
from api.serializers.school import SchoolSerializer


class StudentSerializer(serializers.ModelSerializer):
    classroom = serializers.SerializerMethodField()
    school = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'name', 'classroom_id', 'school_id', 'classroom', 'school', 'createdAt', 'updatedAt')

    def get_classroom(self, obj):
        has_classroom = self.context.get('has_classroom', False)
        if has_classroom:
            return ClassroomSerializer(obj.classroom_id).data
        return None

    def get_school(self, obj):
        has_school = self.context.get('has_school', False)
        if has_school:
            return SchoolSerializer(obj.school_id).data
        return None
