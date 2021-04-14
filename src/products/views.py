from django.core.exceptions import ImproperlyConfigured
from django.contrib import messages
from django.db.models import Q
from django.http import Http404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.reverse import reverse as api_reverse
from rest_framework.views import APIView
from vendor.models import Vendor
from rest_framework.generics import CreateAPIView, ListAPIView,ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from products.serializers import VariationSerializer
from counter.models import Counter
# from store.service import getUserStoreService
# Create your views here.
from .filters import ProductFilter
# from .forms import VariationInventoryFormSet, ProductFilterForm
from .mixins import StaffRequiredMixin
from .models import Product, Variation, Category, ProductFeatured, Company, Brand, GenericName, ProductUnit, ProductCommon, ProductImage, VariationBatch, VariationBatchPrice
from store.models import Store, StoreUser
from .pagination import ProductPagination, CategoryPagination
from .serializers import (
		CategorySerializer, 
		ProductSerializer,
		 ProductDetailSerializer, 
		 ProductDetailUpdateSerializer,
		 ProductFeaturedSerializer,
		 CompanySerializer,
		 BrandSerializer,
		 GenericNameSerializer,
		 ProductUnitSerializer,
		 CommonProductSerializer,
		 AllProductSerializer,
		 AllProductDetailSerializer,
		 ProductVariationSerializer,
		 VariationBatchSerializer
		)

from django.core.exceptions import ValidationError
from rest_framework.exceptions import APIException 
from django.conf import settings







class CommonProductListAPIView(generics.ListAPIView):
	queryset = ProductCommon.objects.all()
	serializer_class = ProductUnitSerializer

class CompanyListAPIView(generics.ListAPIView):
	queryset = Company.objects.all()
	serializer_class = CompanySerializer
	# pagination_class = CategoryPagination

class ProductUnitListAPIView(generics.ListAPIView):
	queryset = ProductUnit.objects.all()
	serializer_class = ProductUnitSerializer
	# pagination_class = CategoryPagination


class BrandListAPIView(generics.ListAPIView):
	queryset = Brand.objects.all()
	serializer_class = BrandSerializer
	# pagination_class = CategoryPagination


class GenericNameListAPIView(generics.ListAPIView):
	queryset = GenericName.objects.all()
	serializer_class = GenericNameSerializer
	# pagination_class = CategoryPagination


class CategoryListAPIView(generics.ListAPIView):
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	pagination_class = CategoryPagination



class CategoryRetrieveAPIView(generics.RetrieveAPIView):
	#authentication_classes = [SessionAuthentication]
	#permission_classes = [IsAuthenticated]
	queryset = Category.objects.all()
	serializer_class = CategorySerializer


class ProductListAPIView(generics.ListAPIView): 
	#permission_classes = [IsAuthenticated]
	queryset = Product.objects.all()
	serializer_class = ProductSerializer
	filter_backends = [
					filters.SearchFilter, 
					filters.OrderingFilter, 
					DjangoFilterBackend
					]
	# search_fields = ["title", "description"] // old version
	filterset_fields = ["title", "description"]
	ordering_fields  = ["title", "id"]
	filter_class = ProductFilter

	def get_queryset(self):
		settings.DLFPRINT()
		queryset = Product.objects.all() ##debug if not working location
		return queryset
		



class ProductRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = ProductDetailSerializer


class ProductVariationRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Variation.objects.all()
	serializer_class = ProductVariationSerializer




class VariationByPatientAPIView(APIView):
	def post(self, request):
		print(request.data)
		p_type = request.data.get('p_type')
		product_id = request.data.get('product_id')
		p_type=5
		variation = Variation.objects.filter(fk_user_type_id=p_type).filter(product_id=product_id).first()
		# print(variation.query())
		return Response(VariationSerializer(variation, read_only=True).data)
from .variationbatch_filter import VariationBatchFilter

class VariationBatchAPIView(APIView):
	queryset = VariationBatch.objects.all()
	serializer_class = VariationBatchSerializer
	filter_class = VariationBatchFilter

	def get(self, request):
		# variation_by_counter = Variation.objects.filter(fk_counter_id=request.session['counter']).values_list('id')
		# print(variation_by_counter)
		adjustment_purpose = request.GET.get('adjustment')
		
		if adjustment_purpose:
			var = Response(VariationBatchSerializer(VariationBatch.objects.all(), many=True).data)
			return var
		return Response(VariationBatchSerializer(VariationBatch.objects.filter(fk_variation__fk_counter_id=request.session['counter']), many=True).data)

	


class VariationBatchViewSet(viewsets.ModelViewSet):
	queryset = VariationBatch.objects.all()
	serializer_class = VariationBatchSerializer

	def list(self, request, **kwargs):
			try:
				music = query_musics_by_args(**request.query_params)
				serializer = VariationBatchSerializer(music['items'], many=True)
				result = dict()
				result['data'] = serializer.data
				result['draw'] = music['draw']
				result['recordsTotal'] = music['total']
				result['recordsFiltered'] = music['count']
				return Response(result, status=status.HTTP_200_OK, template_name=None, content_type=None)

			except Exception as e:
				return Response(e, status=status.HTTP_404_NOT_FOUND, template_name=None, content_type=None)




class VariationBatchPriceAPIView(APIView):
	def get(self, request):
		fk_user_type_id = request.GET.get('fk_user_type_id')
		fk_variation_batch_id = request.GET.get('variation_batch_id')
		variation_batch_price = VariationBatchPrice.objects.filter(fk_variation_batch_id=fk_variation_batch_id).first()
		if fk_user_type_id:
			variation_batch_price = VariationBatchPrice.objects.filter(fk_user_type_id=fk_user_type_id).filter(fk_variation_batch_id=fk_variation_batch_id)
		quantity = 0
		batchno = ''
		expiry_date = ''
		price = 0
		price = VariationBatch.objects.filter(pk=fk_variation_batch_id).first().sale_price
		if variation_batch_price:
			var_batch = variation_batch_price.fk_variation_batch
			if var_batch:
				quantity = var_batch.quantity
				batchno = var_batch.batchno
				expiry_date = var_batch.expiry_date
				price = variation_batch_price.price
		data = {
			'price':price,
			'stock' : quantity,
			"batchno" : batchno
		}
		return Response(data)

	def post(self, request, *args, **kwargs):
			var_batch_price_id = request.data.get('var_batch_price_id') #for edit purpose
			var_batch_price_obj = VariationBatchPrice()
			if var_batch_price_id:
				var_batch_price_obj = VariationBatchPrice.objects.filter(pk=var_batch_price_id).first()	
				if not var_batch_price_obj:
					return Response('Failed to update', status=400)
			price = request.data.get('price')
			fk_variation_batch_id = request.data.get('fk_variation_batch_id')
			fk_user_type_id = request.data.get('fk_user_type_id')

			#check if item price is assign to the type of fk_user_type_id
			check_var_batch_price_obj = VariationBatchPrice.objects.filter(fk_user_type_id=fk_user_type_id).filter(fk_variation_batch_id=fk_variation_batch_id).first()
			if check_var_batch_price_obj:
				return Response('Price already set for this user type', status=400)			
			var_batch_price_obj.fk_variation_batch_id = fk_variation_batch_id
			var_batch_price_obj.price = price
			var_batch_price_obj.sale_price = price
			var_batch_price_obj.fk_user_type_id = fk_user_type_id
			var_batch_price_obj.save()
			return Response('Success', status=200)

# class VariationAPIView(APIView):

	from .pagination import CustomPageNumber

class VariationAPIView(APIView):
	# queryset = Variation.objects.all().order_by('-id')
	# serializer_class = VariationSerializer
	# # filter_class = VariationBatchFilter

	# def get(self, request):
	# 	jptchanges = request.GET.get('jptchanges')
	# 	self.pagination_class = CustomPageNumber
	# 	if jptchanges:
	# 		queryset = self.filter_queryset(self.queryset.filter(title__icontains=jptchanges))
	# 	page = self.paginate_queryset(queryset)
	# 	if page is not None:
	# 		serializer = self.get_serializer(page, many=True)
	# 		return self.get_paginated_response(serializer.data)
	# 	serializer = self.get_serializer(queryset, many=True)
	# 	return Response(serializer.data) 

	serializer_class = VariationSerializer
	def get(self, request):	
		variations = VariationSerializer(Variation.objects.all(), many=True)
		return Response(variations.data, status=200)



class AllProductRetrieveAPIView(generics.RetrieveAPIView):
	queryset = Product.objects.all()
	serializer_class = AllProductDetailSerializer



#### Medical 


class AddProductAPIView(APIView): #VariationAdd
	# authentication_classes = [SessionAuthentication]
	permission_classes = [IsAuthenticated]
	def post(self, request, *args, **kwargs):
		print(request.data)
		variation_id = request.data.get('variation_id')
		product_title = request.data.get('title')					
		category_id = request.data.get('category_id', None)
		brand_id = request.data.get('brand_id', None)
		product_code = request.data.get('product_code', None)
		generic_names_id =request.data.get('generic_names_id', None)
		company_id =request.data.get('company_id', None)
		rack_number =request.data.get('rack_number', None)
		alert_quantity = request.data.get('alert_quantity', None)
		alert_expiry_days = request.data.get('alert_expiry_days', None)
		fk_counter_id = request.data.get('fk_counter_id')
		if product_title is None:
			return Response({"Fail": "Product name must be provided"}, status.HTTP_400_BAD_REQUEST)
		if product_code is None:
			return Response({"Fail": "Product code must be provided"}, status.HTTP_400_BAD_REQUEST)	
		if variation_id:
			product = Variation.objects.filter(pk=variation_id).first()
		else:
			product = Variation()
		product.title = product_title	
		product.generic_name_id = generic_names_id
		product.company_id = company_id
		product.brand_id = brand_id	
		product.code = product_code	
		product.rack_number = rack_number
		product.alert_expiry_days = alert_expiry_days
		product.alert_quantity = alert_quantity
		product.fk_counter_id = fk_counter_id
		product.save()
		if category_id:
			if product.categories:
				cat = product.categories.clear()
			product.categories.add(category_id)
			product.save()
		# product.fk_store_id = fk_store.id	
		return Response({
					'status': True,
					'detail': 'Product Saved successfully'
					})
	def delete(self, request):
		permission_classes = [IsAuthenticated]
		variation_id = request.data.get('variation_id')
		variation = Variation.objects.get(pk=variation_id)
		if variation:
			variation.delete()
			return Response('Product removed successfully', status=200)
		return Response('Error', status=400)



# CBVs

class CategoryListView(ListView):
	model = Category
	queryset = Category.objects.all()
	template_name = "products/product_list.html"


class CategoryDetailView(DetailView):
	model = Category

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = ( product_set | default_products ).distinct()
		context["products"] = products
		return context



import random




class ProductVariationRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = Product
    def get_queryset(self, *args, **kwargs):
        return MembershipType.objects.all()

def hmsproducts(request):
	permission_classes = [IsAuthenticated]
	context = {
		'title' : 'HMS products',
		'products' : Variation.objects.all(),
		'suppliers' : Vendor.objects.all(),
		'manufacturers' : Company.objects.all(),
		'generics' : GenericName.objects.all(),
		'brands' : Brand.objects.all(),
		'counters' : Counter.objects.all(),
	}
	return render(request, "personal/dashboard_layout/products.html", context)

def hmsdruglists(request):
	permission_classes = [IsAuthenticated]
	context = {
			'title' : 'HMS DrugList',
			'products' : Variation.objects.all(),
			'suppliers' : Vendor.objects.all(),
			'manufacturers' : Company.objects.all(),
			'generics' : GenericName.objects.all(),
			'brands' : Brand.objects.all(),
			'counters' : Counter.objects.all(),
		}
	return render(request, "personal/dashboard_layout/hmsdruglists.html", context)
from users.models import UserTypes

def drugprice_special(request):
	permission_classes = [IsAuthenticated]
	context = {
			'title' : 'Price setup / Special Users',
			'usertypes' : UserTypes.objects.all(),
			
		}
	return render(request, "personal/dashboard_layout/special_price.html", context)

from rest_framework.decorators import api_view
@api_view(['GET','POST'])
def hmsproduct_detail(request, id):
	permission_classes = [IsAuthenticated]
	if request.method == 'GET':
		return Response(VariationSerializer(Variation.objects.filter(pk=id), many=True).data)
		# context = {
		# 	'title' : 'HMS products',
		# 	'products' : Variation.objects.all(),
		# 	'suppliers' : Vendor.objects.all(),
		# 	'manufacturers' : Company.objects.all(),
		# 	'generics' : GenericName.objects.all(),
		# 	'brands' : Brand.objects.all(),
		# 	'counters' : Counter.objects.all(),
		# }
		# return render(request, "personal/dashboard_layout/hmsproduct_detail.html", context)


def sales(request):
	permission_classes = [IsAuthenticated]
	context = {
		'title' : 'Sales',
		# 'products' : Variation.objects.all(),
		# 'suppliers' : Vendor.objects.all(),
		# 'manufacturers' : Company.objects.all(),
		# 'generics' : GenericName.objects.all(),
		# 'brands' : Brand.objects.all(),
		# 'counters' : Counter.objects.all(),
	}
	return render(request, "personal/dashboard_layout/sales.html", context)


def hmsvariations(request, id):
	permission_classes = [IsAuthenticated]
	context = {
		'product_id' : id
	}
	return render(request, "personal/dashboard_layout/variation.html", context)

def datatable(request):
	permission_classes = [IsAuthenticated]
	context = {}
	return render(request, "personal/dashboard_layout/datatable.html", context)

def adjustments(request):
	permission_classes = [IsAuthenticated]
	context = {
		'page_title' : 'Adjustments',
		'products' : Variation.objects.all(),
	}
	return render(request, "personal/dashboard_layout/adjustment.html", context)

class PurchaseVariationBatchAPIView(APIView):
	permission_classes = [IsAuthenticated]
	def post(self, request, *args, **kwargs):
		variation_batch = VariationBatch()
		print(request.data)
		variation_batch.fk_variation_id = request.data.get('fk_variation_id')
		variation_batch.batchno = request.data.get('batchno')
		variation_batch.quantity = request.data.get('quantity')
		variation_batch.purchase_date = request.data.get('purchase_date')
		variation_batch.expiry_date = request.data.get('expiration_date')
		variation_batch.use_batch = request.data.get('use_batch')
		variation_batch.price = request.data.get('price')
		variation_batch.save()
		return Response('Success', status=200)

# class VariationBatchPriceAPIView(APIView):
# 	permission_classes = [IsAuthenticated]
# 	def get(self, request, *args, **kwargs):
# 		var_batch_price_id = request.data.get('var_batch_price_id') #for edit purpose
# 		var_batch_price_obj = VariationBatchPrice()
# 		if var_batch_price_id:
# 			var_batch_price_obj = VariationBatchPrice.objects.filter(pk=var_batch_price_id).first()	
# 			if not var_batch_price_obj:
# 				return Response('Failed to update', status=400)
# 		price = request.data.get('price')
# 		fk_variation_batch_id = request.data.get('fk_variation_batch_id')
# 		fk_user_type_id = request.data.get('fk_user_type_id')

# 		#check if item price is assign to the type of fk_user_type_id
# 		check_var_batch_price_obj = VariationBatchPrice.objects.filter(fk_user_type_id=fk_user_type_id).filter(fk_variation_batch_id=fk_variation_batch_id).first()
# 		# if check_var_batch_price_obj:
# 		# 	return Response('Price already set for this user type', status=400)			
# 		var_batch_price_obj.fk_variation_batch_id = fk_variation_batch_id
# 		var_batch_price_obj.price = price
# 		var_batch_price_obj.sale_price = price
# 		var_batch_price_obj.fk_user_type_id = fk_user_type_id
# 		var_batch_price_obj.save()
# 		return Response('Success', status=200)
