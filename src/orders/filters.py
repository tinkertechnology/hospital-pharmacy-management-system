from django_filters import FilterSet, CharFilter, NumberFilter

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