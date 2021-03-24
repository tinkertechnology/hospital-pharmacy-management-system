from django_filters import FilterSet, CharFilter, NumberFilter

from .models import Account, Visit

class VisitFilter(FilterSet):
	patient_fullname = CharFilter(field_name='fk_customer_user__firstname', lookup_expr='icontains', distinct=True)
	visit_id = NumberFilter(field_name='visit_id', lookup_expr='icontains', distinct=True)

	class Meta:
		model = Visit
		fields = [
		# 'patient'
        'patient_fullname',
        'visit_id'
			# 'owner'
		]
