from django_filters import FilterSet, CharFilter, NumberFilter
from carts.models import Cart
# from .models import Account, Visit
from .models import Purchase, Adjustment

class PurchaseFilter(FilterSet):
	class Meta:
		model = Purchase
		fields = [
            'id'
		]




class AdjustmentFilter(FilterSet):
	class Meta:
		model = Adjustment
		fields = [
            'id'
		]


class SalesFilter(FilterSet):
	class Meta:
		model = Cart
		fields = [
            'id'
		]