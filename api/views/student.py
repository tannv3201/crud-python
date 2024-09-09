from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.services.student import get_all_student_service, add_student_service, get_students_service, \
    get_one_student_service, update_student_service, delete_student_service


# ----------------------------------------
# STUDENT API

@api_view(['POST'])
def add_student(request):
    serializer = add_student_service(request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD GET
@api_view(['GET'])
def get_all_student(request):
    serializer = get_all_student_service(request.query_params)
    return Response(serializer.data)


# METHOD GET
@api_view(['GET'])
def get_students(request):
    students = get_students_service(request)

    return students


@api_view(['GET'])
def get_one_student(request, pk):
    serializer = get_one_student_service(request.query_params, pk)
    return Response(serializer.data)


# METHOD UPDATE
@api_view(['PUT', 'PATCH'])
def update_student(request, pk):
    serializer = update_student_service(request.query_params, pk)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# METHOD DELETE
@api_view(['DELETE'])
def delete_student(request, pk):
    delete_student_service(pk)
    return Response(status=status.HTTP_204_NO_CONTENT)
