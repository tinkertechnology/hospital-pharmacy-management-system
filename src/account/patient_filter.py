from django_filters import FilterSet, CharFilter, NumberFilter

from .models import Account

class PatientFilter(FilterSet):
	patient_fullname = CharFilter(field_name='firstname', lookup_expr='icontains')
	customer_id = NumberFilter(field_name='customer_id', lookup_expr='icontains', distinct=True)

	class Meta:
		model = Account
		fields = [
		# 'patient'
        'patient_fullname',
		'customer_id',
        # 'visit_id'
			# 'owner'
		]
