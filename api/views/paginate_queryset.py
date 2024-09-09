from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


def paginate_queryset(request, queryset, serializer_class, context=None, page_size=5, page_size_query_param='pageSize',
                      max_page_size=100, search_param='search', filter_params=None):
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginator.page_size_query_param = page_size_query_param
    paginator.max_page_size = max_page_size

    search = request.query_params.get(search_param, None)

    # Apply filter parameters if provided
    if filter_params:
        updated_filter_params = {}
        for key, value in filter_params.items():
            # Check if the value contains a comma
            if ',' in value:
                # Split the value and use __in to filter
                value_list = [v.strip() for v in value.split(',')]

                updated_filter_params[f"{key}__in"] = value_list
            else:
                updated_filter_params[key] = value

        # Apply the filters to the queryset
        queryset = queryset.filter(**updated_filter_params)

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
