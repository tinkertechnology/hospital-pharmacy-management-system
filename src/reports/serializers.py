
from rest_framework import serializers
from orders.models import *

class ReportSerializer(serializers.ModelSerializer):
	# authentication_classes = [SessionAuthentication, BasicAuthentication]
	# permission_classes = [IsAuthenticated]
	order_total_sum = serializers.IntegerField()
	created_at_date = serializers.DateTimeField()
	class Meta:
		model = StoreWiseOrder
		fields= [
		'order_total_sum',
		'created_at_date',


		]

