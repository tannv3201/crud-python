from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.models.school import School
from api.serializers.school import SchoolSerializer


def add_school_service(data):
    if School.objects.filter(**data).exists():
        return Response({
            'message': 'Dữ liệu trường học đã tồn tại.'
        }, status=status.HTTP_409_CONFLICT)

    school = SchoolSerializer(data=data)

    if school.is_valid():
        school.save()
        return school
    else:
        return None


def get_all_school_service(params):
    if params:
        schools = School.objects.filter(**params.dict()).order_by('-createdAt').values()
        return SchoolSerializer(schools, many=True)
    else:
        schools = School.objects.all().order_by('-createdAt').values()
        return SchoolSerializer(schools, many=True)


def get_schools_service():
    return School.objects.all().order_by('-createdAt').values()


def get_one_school_service(pk):
    school = get_object_or_404(School, pk=pk)
    return SchoolSerializer(school)


def update_school_service(data, pk):
    school = School.objects.get(pk=pk)
    return SchoolSerializer(instance=school, data=data, partial=True)


def delete_school_service(pk):
    school = get_object_or_404(School, pk)
    school.delete()
