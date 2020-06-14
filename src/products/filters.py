from django_filters import FilterSet, CharFilter, NumberFilter

from .models import Product

class ProductFilter(FilterSet):
	title = CharFilter(field_name='title', lookup_expr='icontains', distinct=True)
	category = CharFilter(field_name='categories__title', lookup_expr='icontains', distinct=True)
	category_id = CharFilter(field_name='categories__id', lookup_expr='icontains', distinct=True)
	min_price = NumberFilter(field_name='variation__price', lookup_expr='gte', distinct=True) # (some_price__gte=somequery)
	max_price = NumberFilter(field_name='variation__price', lookup_expr='lte', distinct=True)
	brand_id = CharFilter(field_name='brand__id', lookup_expr='icontains', distinct=True)
	generic_name_id = CharFilter(field_name='generic_name__id', lookup_expr='icontains', distinct=True)
	company_id = CharFilter(field_name='company__id', lookup_expr='icontains', distinct=True)
	amount = CharFilter(field_name='amount', lookup_expr='icontains', distinct=True)
	product_unit_id = CharFilter(field_name='product_unit__id', lookup_expr='icontains', distinct=True)
	sale_price_gt = NumberFilter(field_name='variation__sale_price', lookup_expr='gt', distinct=True)
	fk_store = NumberFilter(field_name='fk_store__id', lookup_expr='icontains', distinct=True)
	# owner = NumberFilter(field_name='fk_store__id', lookup_expr='icontains', distinct=True)
	


	class Meta:
		model = Product
		fields = [
			'min_price',
			'max_price',
			'category',
			'title',
			'description',
			'company_id',
			'generic_name_id',
			'brand_id',
			'amount',
			'product_unit_id',
			'sale_price_gt',
			'fk_store',
			# 'owner'
		]