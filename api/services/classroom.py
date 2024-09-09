from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.models.classroom import Classroom
from api.serializers.classroom import ClassroomSerializer
from api.views.paginate_queryset import paginate_queryset


def add_classroom_service(data):
    if Classroom.objects.filter(**data).exists():
        return Response({
            'message': 'Dữ liệu lớp hoọc đã tồn tại.'
        }, status=status.HTTP_409_CONFLICT)

    serializer = ClassroomSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return serializer
    else:
        return None


def get_all_classroom_service(params):
    has_school = params.get('has_school', 'false').lower() == 'true'

    filter_params = {key: value for key, value in params.items() if key in ['school']}

    schools = Classroom.objects.filter(**filter_params).select_related('school_id').order_by('-createdAt')

    return ClassroomSerializer(schools, many=True, context={'has_school': has_school})


def get_classrooms_service(request):
    filter_params = {key: value for key, value in request.query_params.items() if
                     key in ['school_id']}
    context = {'has_school': request.query_params.get('has_school', 'false').lower() == 'true'}

    queryset = Classroom.objects.all().select_related('school_id').order_by(
        '-createdAt')  # select_related: lấy thông tin của bảng liên quan school

    return paginate_queryset(request, queryset, ClassroomSerializer, context=context, filter_params=filter_params)


def get_one_classroom_service(request, pk):
    # checking for the parameters from the URL
    has_school = request.query_params.get('has_school', 'false').lower() == 'true'

    class_data = get_object_or_404(Classroom, pk=pk)

    return ClassroomSerializer(class_data, context={'has_school': has_school})


def update_classroom_service(data, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    return ClassroomSerializer(instance=classroom, data=data, partial=True)


def delete_classroom_service(pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    classroom.delete()
