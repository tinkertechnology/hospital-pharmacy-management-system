from django_filters import FilterSet, CharFilter, NumberFilter

from .models import Account, Visit

class VisitFilter(FilterSet):
	fk_customer_user = CharFilter(field_name='fk_customer_user__firstname', lookup_expr='icontains', distinct=True)

	class Meta:
		model = Visit
		fields = [
		# 'patient'
        'fk_customer_user'
			# 'owner'
		]
