# from django_filters import FilterSet
import django_filters
from rest_framework import filters
from rest_framework import serializers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Variation, VariationBatch, VariationBatchPrice
from products.filters import VariationFilter
from .variationbatch_filter import VariationBatchFilter, VariationBatchPriceFilter
from rest_framework import pagination
from rest_framework.response import Response

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
    

class VariationDataTableSerializer(serializers.ModelSerializer):
	class Meta:
		model = Variation
		fields= '__all__'

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
            'recordsFiltered' : self.page.paginator.count,
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
    filterset_class = VariationFilter

    filter_backends = [
                filters.SearchFilter, 
                filters.OrderingFilter, 
                DjangoFilterBackend
                ]
    # search_fields = ["title", "description"] // old version
    filterset_fields = ["title"]
    ordering_fields  = ["title", "id"]
    #ordering_fields = '__all__'
    # filterset_fields = ['title']
    #ordering = ['id']
    def get_queryset(self):
        print(self.request)
        return Variation.objects.all().order_by('-id')



class VariationBatchDataTableSerializer(serializers.ModelSerializer):
    code = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    generic_name = serializers.SerializerMethodField()
    rack_no = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()
    class Meta:
        model = VariationBatch
        fields= '__all__'
    
    def get_code(self, obj):
        code = "N/A"
        if obj.fk_variation:
            code = obj.fk_variation.code
        return code
    def get_title(self, obj):
        title = "N/A"
        if obj.fk_variation:
            title = obj.fk_variation.title
        return title

    def get_generic_name(self, obj):
        generic_name = "N/A"
        if obj.fk_variation:
            if obj.fk_variation.generic_name:
                generic_name = obj.fk_variation.generic_name.title
        return generic_name
    def get_rack_no(self, obj):
        rack_no = "N/A"
        if obj.fk_variation:            
            rack_no = obj.fk_variation.rack_number
        return rack_no   
    def get_company_name(self, obj):
        company_name = "N/A"
        if obj.fk_variation:
            if obj.fk_variation.company:
                generic_name = obj.fk_variation.company.title
        return company_name    

class VariationBatchTable(generics.ListAPIView):
    serializer_class = VariationBatchDataTableSerializer
    pagination_class = DataTablePagination
    filterset_class = VariationBatchFilter

    filter_backends = [
                filters.SearchFilter, 
                filters.OrderingFilter, 
                DjangoFilterBackend
                ]
    # search_fields = ["title", "description"] // old version
    filterset_fields = ["fk_variation__title"]
    ordering_fields  = ["id"]
    #ordering_fields = '__all__'
    # filterset_fields = ['title']
    #ordering = ['id']
    def get_queryset(self):
        print(self.request)
        return VariationBatch.objects.all().order_by('-id')




class VariationBatchPriceDataTableSerializer(serializers.ModelSerializer):
    # code = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    # generic_name = serializers.SerializerMethodField()
    # rack_no = serializers.SerializerMethodField()
    # company_name = serializers.SerializerMethodField()

    class Meta:
        model = VariationBatchPrice
        fields= '__all__'
    
    # def get_code(self, obj):
    #     code = "N/A"
    #     if obj.fk_variation:
    #         code = obj.fk_variation.code
    #     return code
    def get_title(self, obj):
        title = "N/A"
        if obj.fk_variation_batch:
            if obj.fk_variation_batch.fk_variation:
                title = obj.fk_variation_batch.fk_variation.title
        return title

    def get_user_type(self, obj):
        user_type = "N/A"
        if obj.fk_user_type:
            user_type = obj.fk_user_type.title
        return user_type
    # def get_rack_no(self, obj):
    #     rack_no = "N/A"
    #     if obj.fk_variation:            
    #         rack_no = obj.fk_variation.rack_number
    #     return rack_no   
    # def get_company_name(self, obj):
    #     company_name = "N/A"
    #     if obj.fk_variation:
    #         if obj.fk_variation.company:
    #             generic_name = obj.fk_variation.company.title
    #     return company_name    




class VariationBatchPriceTable(generics.ListAPIView): #Special_Price
    serializer_class = VariationBatchPriceDataTableSerializer
    pagination_class = DataTablePagination
    filterset_class = VariationBatchPriceFilter

    filter_backends = [
                filters.SearchFilter, 
                filters.OrderingFilter, 
                DjangoFilterBackend
                ]
    # search_fields = ["title", "description"] // old version
    filterset_fields = ["fk_variation__title"]
    ordering_fields  = ["id"]
    #ordering_fields = '__all__'
    # filterset_fields = ['title']
    #ordering = ['id']
    def get_queryset(self):
        print(self.request)
        return VariationBatchPrice.objects.all().order_by('-id')