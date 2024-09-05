from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from .models import Item, School, ClassRoom, Student
from .serlializers import ItemSerializer, SchoolSerializer, ClassRoomSerializer, StudentSerializer


# METHOD GET
@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Search by Category': '/?category=category_name',
        'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)


# METHOD POST
@api_view(['POST'])
def add_items(request):
    item = ItemSerializer(data=request.data)

    # validating for already existing data
    if Item.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# METHOD GET
@api_view(['GET'])
def view_items(request):
    # checking for the parameters from the URL
    if request.query_params:
        items = Item.objects.filter(**request.query_params.dict())
    else:
        items = Item.objects.all()

    # if there is something in items else raise error
    if items:
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# METHOD UPDATE
@api_view(['POST'])
def update_items(request, pk):
    item = Item.objects.get(pk=pk)
    print("abc", item)
    data = ItemSerializer(instance=item, data=request.data)
    print("data", data.is_valid())
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


# METHOD DELETE
@api_view(['DELETE'])
def delete_items(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return Response(status=status.HTTP_202_ACCEPTED)


# ----------------------------------------
# SCHOOL API

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
        schools = School.objects.filter(**request.query_params.dict())
    else:
        schools = School.objects.all()

    # if there is something in schools else raise error
    serializer = SchoolSerializer(schools, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_schools(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Số lượng bản ghi trên mỗi trang
    paginator.page_size_query_param = 'pageSize'
    paginator.max_page_size = 100  # Số lượng bản ghi tối đa trên mỗi trang

    search = request.query_params.get('search', None)  # Thêm tham số tìm kiếm

    filter_params = {}
    for param in request.query_params:
        if param not in ['page', 'pageSize', 'search']:  # Loại trừ các tham số phân trang
            filter_params[param] = request.query_params.get(param)

    schools = School.objects.filter(**filter_params)

    if search:
        schools = schools.filter(name__icontains=search)  # Tìm kiếm không phân biệt chữ hoa chữ thường

    result_page = paginator.paginate_queryset(schools, request)
    serializer = SchoolSerializer(result_page, many=True)

    response_data = {
        'totalRecords': schools.count(),
        'totalPages': paginator.page.paginator.num_pages,
        'currentPage': paginator.page.number,
        'pageSize': paginator.page.paginator.per_page,
        'results': serializer.data
    }
    return Response(response_data)


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
def add_class(request):
    class_data = ClassRoomSerializer(data=request.data)
    print(class_data)

    # validating for already existing data

    if ClassRoom.objects.filter(**request.data).exists():
        raise serializers.ValidationError('This data already exists')

    if class_data.is_valid():
        class_data.save()
        return Response(class_data.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD GET
@api_view(['GET'])
def get_all_class(request):
    has_school = request.query_params.get('has_school', 'false').lower() == 'true'

    filter_params = {key: value for key, value in request.query_params.items() if key in ['school']}

    schools = ClassRoom.objects.filter(**filter_params)

    serializer = ClassRoomSerializer(schools, many=True, context={'has_school': has_school})
    return Response(serializer.data)


# METHOD GET
@api_view(['GET'])
def get_classes(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5  # Số lượng bản ghi trên mỗi trang
    paginator.page_size_query_param = 'pageSize'
    paginator.max_page_size = 100  # Số lượng bản ghi tối đa trên mỗi trang

    search = request.query_params.get('search', None)  # Thêm tham số tìm kiếm
    school_id = request.query_params.get('school_id', None)  # Thêm tham số tìm kiếm

    filter_params = {}
    for param in request.query_params:
        if param not in ['page', 'pageSize']:  # Loại trừ các tham số phân trang
            filter_params[param] = request.query_params.get(param)

    has_school = request.query_params.get('has_school', 'false').lower() == 'true'

    filter_params = {key: value for key, value in request.query_params.items() if key in ['school_id']}

    classes = ClassRoom.objects.filter(**filter_params)

    if search:
        classes = classes.filter(name__icontains=search)  # Tìm kiếm không phân biệt chữ hoa chữ thường

    if school_id:
        classes = classes.filter(school_id=school_id)  # Tìm kiếm không phân biệt chữ hoa chữ thường

    result_page = paginator.paginate_queryset(classes, request)

    serializer = ClassRoomSerializer(result_page, many=True, context={'has_school': has_school})

    response_data = {
        'totalRecords': classes.count(),
        'totalPages': paginator.page.paginator.num_pages,
        'currentPage': paginator.page.number,
        'pageSize': paginator.page.paginator.per_page,
        'results': serializer.data
    }
    return Response(response_data)


@api_view(['GET'])
def get_one_class(request, pk):
    # checking for the parameters from the URL
    has_school = request.query_params.get('has_school', 'false').lower() == 'true'

    class_data = get_object_or_404(ClassRoom, pk=pk)

    serializer = ClassRoomSerializer(class_data, context={'has_school': has_school})
    return Response(serializer.data)


# METHOD UPDATE
@api_view(['PUT', 'PATCH'])
def update_class(request, pk):
    class_data = ClassRoom.objects.get(pk=pk)
    data = ClassRoomSerializer(instance=class_data, data=request.data, partial=True)
    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD DELETE
@api_view(['DELETE'])
def delete_class(request, pk):
    class_data = get_object_or_404(ClassRoom, pk=pk)
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

    filter_params = {key: value for key, value in request.query_params.items() if key in ['class_id']}

    students = Student.objects.filter(**filter_params)

    serializer = StudentSerializer(students, many=True, context={'has_class': has_class})
    return Response(serializer.data)


# METHOD GET
@api_view(['GET'])
def get_students(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    paginator.page_size_query_param = 'pageSize'
    paginator.max_page_size = 100

    search = request.query_params.get('search', None)  # Thêm tham số tìm kiếm
    class_id = request.query_params.get('class_id', None)  # Thêm tham số tìm kiếm

    filter_params = {}
    for param in request.query_params:
        if param not in ['page', 'pageSize', 'search', 'class_id']:  # Loại trừ các tham số phân trang
            filter_params[param] = request.query_params.get(param)

    has_class = request.query_params.get('has_class', 'false').lower() == 'true'

    filter_params = {key: value for key, value in request.query_params.items() if key in ['class_id']}

    students = Student.objects.filter(**filter_params)

    if search:
        students = students.filter(name__icontains=search)  # Tìm kiếm không phân biệt chữ hoa chữ thường

    if class_id:
        students = students.filter(class_id=class_id)  # Tìm kiếm không phân biệt chữ hoa chữ thường

    result_page = paginator.paginate_queryset(students, request)

    serializer = StudentSerializer(result_page, many=True, context={'has_class': has_class})

    response_data = {
        'totalRecords': students.count(),
        'totalPages': paginator.page.paginator.num_pages,
        'currentPage': paginator.page.number,
        'pageSize': paginator.page.paginator.per_page,
        'results': serializer.data
    }
    return Response(response_data)


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
