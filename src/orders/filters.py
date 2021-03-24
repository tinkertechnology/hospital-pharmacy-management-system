from django_filters import FilterSet, CharFilter, NumberFilter

# from .models import Account, Visit
from .models import Purchase

class PurchaseFilter(FilterSet):
	class Meta:
		model = Purchase
		fields = [
            'id'
		]
