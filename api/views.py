from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import School, Classroom, Student
from .serlializers import SchoolSerializer, ClassroomSerializer, StudentSerializer


def paginate_queryset(request, queryset, serializer_class, context=None, page_size=5, page_size_query_param='pageSize',
                      max_page_size=100, search_param='search', filter_params=None):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginator.page_size_query_param = page_size_query_param
    paginator.max_page_size = max_page_size

    search = request.query_params.get(search_param, None)

    # Apply filter parameters if provided
    if filter_params:
        queryset = queryset.filter(**filter_params)

    if search:
        queryset = queryset.filter(name__icontains=search)

    result_page = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(result_page, many=True, context=context)

    response_data = {
        'totalRecords': queryset.count(),
        'totalPages': paginator.page.paginator.num_pages,
        'currentPage': paginator.page.number,
        'pageSize': paginator.page.paginator.per_page,
        'results': serializer.data
    }
    return Response(response_data)


# ----------------------------------------
# SCHOOL API

class BasePagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'pageSize'
    max_page_size = 100


def paginate_and_respond(queryset, request, serializer_class, context=None):
    paginator = BasePagination()
    result_page = paginator.paginate_queryset(queryset, request)
    serializer = serializer_class(result_page, many=True, context=context)
    return paginator.get_paginated_response(serializer.data)


@api_view(['POST'])
def add_school(request):
    school = SchoolSerializer(data=request.data)

    # validating for already existing data

    if School.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if school.is_valid():
        school.save()
        return Response(school.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD GET
@api_view(['GET'])
def get_all_school(request):
    # checking for the parameters from the URL
    if request.query_params:
        schools = School.objects.filter(**request.query_params.dict()).order_by('-createdAt').values()
    else:
        schools = School.objects.all().order_by('-createdAt').values()

    # if there is something in schools else raise error
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_schools(request):
    queryset = School.objects.all().order_by('-createdAt').values()

    return paginate_queryset(request, queryset, SchoolSerializer, context=None, filter_params=None)


@api_view(['GET'])
def get_one_school(request, pk):
    school = get_object_or_404(School, pk=pk)

    serializer = SchoolSerializer(school)
    return Response(serializer.data)


# METHOD UPDATE
@api_view(['PUT', 'PATCH'])
def update_school(request, pk):
    school = School.objects.get(pk=pk)
    data = SchoolSerializer(instance=school, data=request.data, partial=True)
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD DELETE
@api_view(['DELETE'])
def delete_school(request, pk):
    school = get_object_or_404(School, pk=pk)
    school.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------------------------------
# CLASS API
@api_view(['POST'])
def create_classroom(request):
    class_data = ClassroomSerializer(data=request.data)

    if Classroom.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if class_data.is_valid():
        class_data.save()
        return Response(class_data.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD GET
@api_view(['GET'])
def get_all_classroom(request):
    has_school = request.query_params.get('has_school', 'false').lower() == 'true'

    filter_params = {key: value for key, value in request.query_params.items() if key in ['school']}

    schools = Classroom.objects.filter(**filter_params).select_related('school_id').order_by('-createdAt')

    serializer = ClassroomSerializer(schools, many=True, context={'has_school': has_school})
    return Response(serializer.data)


# METHOD GET
@api_view(['GET'])
def get_classrooms(request):
    filter_params = {key: value for key, value in request.query_params.items() if
                     key in ['school_id']}
    context = {'has_school': request.query_params.get('has_school', 'false').lower() == 'true'}

    queryset = Classroom.objects.all().select_related('school_id').order_by(
        '-createdAt')  # select_related: lấy thông tin của bảng liên quan school
    return paginate_queryset(request, queryset, ClassroomSerializer, context=context, filter_params=filter_params)


@api_view(['GET'])
def get_one_classroom(request, pk):
    # checking for the parameters from the URL
    has_school = request.query_params.get('has_school', 'false').lower() == 'true'

    class_data = get_object_or_404(Classroom, pk=pk)

    serializer = ClassroomSerializer(class_data, context={'has_school': has_school})
    return Response(serializer.data)


# METHOD UPDATE
@api_view(['PUT', 'PATCH'])
def update_classroom(request, pk):
    class_data = Classroom.objects.get(pk=pk)
    data = ClassroomSerializer(instance=class_data, data=request.data, partial=True)
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD DELETE
@api_view(['DELETE'])
def delete_classroom(request, pk):
    class_data = get_object_or_404(Classroom, pk=pk)
    class_data.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ----------------------------------------
# STUDENT API

@api_view(['POST'])
def add_student(request):
    student = StudentSerializer(data=request.data)
    # validating for already existing data

    # if Student.objects.filter(**request.data).exists():
    #     raise serializers.ValidationError('This data already exists')

    if student.is_valid():
        student.save()
        return Response(student.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD GET
@api_view(['GET'])
def get_all_student(request):
    has_class = request.query_params.get('has_class', 'false').lower() == 'true'

    filter_params = {key: value for key, value in request.query_params.items() if key in ['classroom_id']}

    students = Student.objects.filter(**filter_params).select_related('classroom_id').order_by('-createdAt')

    serializer = StudentSerializer(students, many=True, context={'has_class': has_class})
    return Response(serializer.data)


# METHOD GET
@api_view(['GET'])
def get_students(request):
    filter_params = {key: value for key, value in request.query_params.items() if
                     key in ['classroom_id', 'school_id', 'classroom']}

    school_id = filter_params.get('school_id')
    # students = Student.objects.select_related('classroom__school').filter(classroom__school_id=school_id)

    if school_id:
        queryset = Student.objects.select_related('classroom_id__school_id') \
            .filter(classroom_id__school_id=school_id) \
            .order_by('-createdAt')
        filter_params.pop("school_id", None)
    else:
        all_student = Student.objects.all()
        queryset = all_student.select_related('classroom_id').order_by('-createdAt')

    context = {'has_classroom': request.query_params.get('has_classroom', 'false').lower() == 'true',
               'has_school': request.query_params.get('has_school', 'false').lower() == 'true'}

    return paginate_queryset(request, queryset, StudentSerializer, context=context, filter_params=filter_params)


@api_view(['GET'])
def get_one_student(request, pk):
    # checking for the parameters from the URL
    has_class = request.query_params.get('has_class', 'false').lower() == 'true'

    student = get_object_or_404(Student, pk=pk)

    serializer = StudentSerializer(student, context={'has_class': has_class})
    return Response(serializer.data)


# METHOD UPDATE
@api_view(['PUT', 'PATCH'])
def update_student(request, pk):
    student = Student.objects.get(pk=pk)
    data = StudentSerializer(instance=student, data=request.data, partial=True)
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)


# METHOD DELETE
@api_view(['DELETE'])
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
