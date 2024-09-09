from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers.school import SchoolSerializer
from api.services.school import add_school_service, get_all_school_service, get_schools_service, get_one_school_service, \
    update_school_service, delete_school_service
from api.views.paginate_queryset import paginate_queryset


@api_view(['POST'])
def add_school(request):
    serializer = add_school_service(request.data)

    if serializer:
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD GET
@api_view(['GET'])
def get_all_school(request):
    serializer = get_all_school_service(request.query_params)
    return Response(serializer.data)


@api_view(['GET'])
def get_schools(request):
    queryset = get_schools_service()

    return paginate_queryset(request, queryset, SchoolSerializer, context=None, filter_params=None)


@api_view(['GET'])
def get_one_school(request, pk):
    serializer = get_one_school_service(pk)
    return Response(serializer.data)


# METHOD UPDATE
@api_view(['PUT', 'PATCH'])
def update_school(request, pk):
    serializer = update_school_service(request.data, pk)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


# METHOD DELETE
@api_view(['DELETE'])
def delete_school(request, pk):
    delete_school_service(pk)
    return Response(status=status.HTTP_204_NO_CONTENT)
