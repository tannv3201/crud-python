from rest_framework import serializers

from api.models.classroom import Classroom
from api.serializers.school import SchoolSerializer


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
