from rest_framework import pagination


class PageNumberPaginationWithLimit(pagination.PageNumberPagination):
    """Pagination class with page size query param """
    page_size_query_param = 'limit'
