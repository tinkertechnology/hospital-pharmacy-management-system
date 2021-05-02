# from django_filters import FilterSet
import django_filters
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import Account
from rest_framework import pagination
from rest_framework.response import Response
from .patient_filter import PatientFilter
from users.models import UserType


# class UsersDataTableFilterSet(django_filters.FilterSet):
#     class Meta:
#         model = Visit
#         fields= '__all__'
#         # maybe works
        #exclude=''
        #
        #fields=None
        #fields=['id'] #works
        #fields=None
        #filter_fields = __all__

# class ProductFilter(django_filters.FilterSet):
#     # name = django_filters.CharFilter(lookup_expr='iexact')

#     class Meta:
#         model = Variation
#         fields = ['title']
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
from dateutil.relativedelta import relativedelta
from datetime import datetime
class PatientDataTableSerializer(serializers.ModelSerializer):
    patient_fullname = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()
    last_visit = serializers.SerializerMethodField()
    user_type = serializers.SerializerMethodField()
    class Meta:
        model = Account
        fields= '__all__'

    def get_patient_fullname(self, obj):
        fullname = ""
        if obj.firstname:
            fullname += obj.firstname
        if obj.lastname:
            fullname += ' '+obj.lastname
        return fullname

    def get_gender(self, obj):
        gender = ""
        if obj.fk_gender:
           gender = obj.fk_gender.title
        return gender
    

    def get_age(self, obj):
        delta = 'N/A'
        if obj.date_of_birth:
            delta = relativedelta(datetime.now().date(), obj.date_of_birth) 
            return str(delta.years) + ' years'
        return delta
    def get_user_type(self, obj):
        user_type = 'N/A'
        user_type_obj = UserType.objects.filter(user=obj).first()
        if user_type_obj:
            user_type_obj = user_type_obj.user_type
            if user_type_obj:
                user_type = user_type_obj.title
        return user_type
    
    def get_last_visit(self, obj):
        last_visit = ""
        last_visit_obj = obj.fk_customer_user.first() #order_by('-timestamp').first()
        print('last-visit', last_visit_obj)
            # print('last', last_visit)
        if last_visit_obj:
            last_visit = last_visit_obj.timestamp.strftime("%Y-%m-%d, %I:%M %p")
        return last_visit

    # def get_visit_type(self,obj):
    #     visit_type = ''
    #     # if obj.fk_visit:
    #     #     return obj.fk_visit.title
    #     if obj.fk_customer_user: #visit ma
    #         visit = obj.fk_customer_user.fk_visit
    #         if visit:
    #             visit_type = visit.title
    #     return visit_type

            




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
        # print("print(page_size, start, page_number)")
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
class PatientDataTable(generics.ListAPIView):
    serializer_class = PatientDataTableSerializer
    pagination_class = DataTablePagination
    filterset_class = PatientFilter

    filter_backends = [
                filters.SearchFilter, 
                filters.OrderingFilter, 
                DjangoFilterBackend
                ]
    # search_fields = ["title", "description"] // old version
    filterset_fields = ["firstname"]
    ordering_fields  = ["-id"]
    #ordering_fields = '__all__'
    # filterset_fields = ['title']
    #ordering = ['id']
    def get_queryset(self):
        # print(self.request)
        pids = UserType.objects.all()
        patients = Account.objects.filter(pk__in=pids.values('user_id'))
        return patients#Account.objects.all().order_by('-id')




