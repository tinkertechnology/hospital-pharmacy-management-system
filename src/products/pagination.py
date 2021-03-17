from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework import pagination
from rest_framework.response import Response
from collections import OrderedDict


class ProductPagination(LimitOffsetPagination):
	default_limit = 10
	max_limit = 500
	limit_query_param = "limit"
	offset_query_param = "offset"




class CategoryPagination(LimitOffsetPagination):
	default_limit = 20
	max_limit = 20
	limit_query_param = "limit"
	offset_query_param = "offset"


class WSCPagination(LimitOffsetPagination):
	default_limit = 20
	max_limit = 20
	limit_query_param = "limit"
	offset_query_param = "offset"


class CustomPageNumber(pagination.PageNumberPagination):
    page_size = 2

    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('lastPage', self.page.paginator.count),
             ('countItemsOnPage', self.page_size),
             ('current', self.page.number),
             ('next', self.get_next_link()),
			 ('count', self.page.paginator.count),
             ('previous', self.get_previous_link()),
			 ('page', self.page.number),
			 ('num_page', self.page.paginator.num_pages),
             ('results', data)
         ]))