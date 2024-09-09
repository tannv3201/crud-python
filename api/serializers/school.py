from rest_framework import serializers

from api.models.school import School


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name', 'address', 'createdAt', 'updatedAt')
