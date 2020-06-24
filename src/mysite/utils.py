from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from users.models import UserType
from store.models import Store
from wsc.models import WaterSupplyCompany
#from orders.models import UserCheckout

def jwt_response_payload_handler(token, user, request, *args, **kwargs):

	user_type=None
	is_depo = None
	is_supply_company = None

	user_type1 = UserType.objects.filter(user=user.id).first()

	depo =  Store.objects.filter(fk_user_id=user.id).filter(fk_store_type_id=2).first()
	is_supply_company = Store.objects.filter(fk_user_id=user.id).filter(fk_store_type_id=1).first()
	if is_supply_company is not None:
		is_supply_company = True
	
	if depo is not None:
		is_depo = True
	# print(user.__dict__)
	# if 'usertype' in user.__dict__ :
	if user_type1:
		user_type = user.usertype.user_type.title
	# print(user.usertype.user_type.title)
	# user_type=""
	# try:
	# 	user_type=user.usertype.user_type.title
	# 	return user_type
	# except ObjectDoesNotExist:
	# 	user_type=""
	# 	return user_type
	
	
	data = {
		"user_type": user_type,
		"is_depo": is_depo,
		"is_supply_company" : is_supply_company,
		# "user_description": user.usertype,
		"token": token,
		"user": user.id,
		"username": user.username,
		"email": user.email,
		"mobile": user.mobile,
		"superuser" : user.is_superuser,
		'code': 20000,
		"staff": user.is_staff,
		# 'first_name': user.first_name,
		# 'last_name': user.last_name,
		"orig_iat": timezone.now(),
		#"user_braintree_id": UserCheckout.objects.get(user=user).get_braintree_id
	}
	return data
