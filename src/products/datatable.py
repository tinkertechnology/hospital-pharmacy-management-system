# from django_filters import FilterSet
import django_filters

from rest_framework import generics
from .models import Variation

class UsersDataTableFilterSet(django_filters.FilterSet):
    class Meta:
        model = Variation
        fields= '__all__'
        # maybe works
        #exclude=''
        #
        #fields=None
        #fields=['id'] #works
        #fields=None
        #filter_fields = __all__

class ProductFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Variation
        fields = ['title']
# class VariationDataTableFilterSet(FilterSet):
#     class Meta:
#         model = Variation
#         # fields= '__all__'
#         # maybe works
#         # exclude=''
#         #
#         #fields=None
#         fields=['title'] #works
#         #fields=None
#         #filter_fields = __all__
    

from rest_framework import serializers
class VariationDataTableSerializer(serializers.ModelSerializer):
	class Meta:
		model = Variation
		fields= '__all__'
from rest_framework import pagination
from rest_framework.response import Response
# https://github.com/encode/django-rest-framework/blob/master/rest_framework/pagination.py
# see fields to overide from PageNumberPagination
class DataTablePagination(pagination.PageNumberPagination):
    page_size = 100
    #page_size_query_param = 'page_size'
    page_size_query_param = 'length'
    max_page_size = 1000

    # Client can control the page using this query parameter.
    #page_query_param = 'page'
    #page_query_param = 'draw'

    # copied form
    #.venv\Lib\site-packages\rest_framework\pagination.py
    #
    # on upgraded djano rest framework, can override get_page_number only
    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        # page_number = request.query_params.get(self.page_query_param, 1)
        page_number = self.get_page_number(request, paginator) #changed on new django
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        #except InvalidPage as exc:
        except Exception as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message='six.text_type(exc)'
            )
            raise exc
            #raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    # on new django can override this only
    def get_page_number(self, request, paginator):
    	#datatable sends start and length
        page_size = request.query_params.get('length', 1)
        start = request.query_params.get('start', 0)
        
        page_number = int(start)/int(page_size)
        page_number += 1 # (pgno starts from 1 to n) not 0 to n-1
        # page_number= page_number if page_number else 1
        
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        print("print(page_size, start, page_number)")
        print(page_size, start, page_number)
        return page_number

    def get_paginated_response(self, data):
        #print(data)
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'recordsTotal': self.page.paginator.count,
            # 'recordsFiltered' : 
            'data': data
        })

from rest_framework.generics import  ListAPIView
# from users.views import ( UsersDataTable )
# urlpatterns += [ re_path(r'^api/UsersDataTable/$', UsersDataTable.as_view(), name="inquiry_user"), ]
# 
# /api/UsersDataTable?id=
class VariationDataTable(generics.ListAPIView):
    serializer_class = VariationDataTableSerializer
    pagination_class = DataTablePagination
    filterset_class = ProductFilter
    #ordering_fields = '__all__'
    # filterset_fields = ['title']
    #ordering = ['id']
    def get_queryset(self):
        print(self.request)
        return Variation.objects.all()