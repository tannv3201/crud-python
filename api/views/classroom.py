from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.services.classroom import add_classroom_service, get_all_classroom_service, get_classrooms_service, \
    get_one_classroom_service, update_classroom_service, delete_classroom_service


# ----------------------------------------
# CLASS API
@api_view(['POST'])
def create_classroom(request):
    serializer = add_classroom_service(request.data)

    if serializer.is_valid():
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD GET
@api_view(['GET'])
def get_all_classroom(request):
    serializer = get_all_classroom_service(request.query_params)
    return Response(serializer.data)


# METHOD GET
@api_view(['GET'])
def get_classrooms(request):
    classrooms = get_classrooms_service(request)
    return classrooms


@api_view(['GET'])
def get_one_classroom(request, pk):
    classroom = get_one_classroom_service(request, pk)
    return Response(classroom.data)


# METHOD UPDATE
@api_view(['PUT', 'PATCH'])
def update_classroom(request, pk):
    classroom = update_classroom_service(request.data, pk)
    if classroom.is_valid():
        classroom.save()
        return Response(classroom.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD DELETE
@api_view(['DELETE'])
def delete_classroom(request, pk):
    delete_classroom_service(pk)
    return Response(status=status.HTTP_204_NO_CONTENT)
