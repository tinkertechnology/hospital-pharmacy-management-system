from django_filters import FilterSet, CharFilter, NumberFilter

from .models import VariationBatch, VariationBatchPrice

class VariationBatchFilter(FilterSet):
	fk_variation = CharFilter(field_name='fk_variation__title', lookup_expr='icontains', distinct=True)
	# owner = NumberFilter(field_name='fk_store__id', lookup_expr='icontains', distinct=True)
	


	class Meta:
		model = VariationBatch
		fields = [			
			'fk_variation',
			# 'owner'
		]


class VariationBatchPriceFilter(FilterSet):
	fk_variation = CharFilter(field_name='fk_variation__title', lookup_expr='icontains', distinct=True)
	# owner = NumberFilter(field_name='fk_store__id', lookup_expr='icontains', distinct=True)
	


	class Meta:
		model = VariationBatchPrice
		fields = [			
			'fk_variation',
			# 'owner'
		]