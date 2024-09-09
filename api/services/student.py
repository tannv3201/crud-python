from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response

from api.models.student import Student
from api.serializers.student import StudentSerializer
from api.views.paginate_queryset import paginate_queryset


def add_student_service(data):
    if Student.objects.filter(**data).exists():
        return Response({
            'message': 'Dữ liệu học sinh đã tồn tại.'
        }, status=status.HTTP_409_CONFLICT)

    serializer = StudentSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return serializer
    else:
        return None


def get_all_student_service(params):
    filter_params = {key: value for key, value in params.items() if key in ['classroom_id']}

    students = Student.objects.filter(**filter_params).select_related('classroom_id').order_by('-createdAt')

    return StudentSerializer(students, many=True)


def get_students_service(request):
    filter_params = {key: value for key, value in request.query_params.items() if
                     key in ['classroom_id', 'school_id', 'classroom']}

    all_student = Student.objects.all()
    queryset = all_student.select_related('classroom_id', 'school_id').order_by('-createdAt')

    context = {'has_classroom': request.query_params.get('has_classroom', 'false').lower() == 'true',
               'has_school': request.query_params.get('has_school', 'false').lower() == 'true'}

    return paginate_queryset(request, queryset, StudentSerializer, context=context, filter_params=filter_params)


def get_one_student_service(params, pk):
    has_class = params.get('has_class', 'false').lower() == 'true'

    student = get_object_or_404(Student, pk=pk)

    return StudentSerializer(student, context={'has_class': has_class})


def update_student_service(data, pk):
    student = Student.objects.get(pk=pk)
    return StudentSerializer(instance=student, data=data, partial=True)


def delete_student_service(pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
