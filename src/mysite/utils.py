from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from users.models import UserType
#from orders.models import UserCheckout

def jwt_response_payload_handler(token, user, request, *args, **kwargs):

	user_type=""
	user_type1 = UserType.objects.filter(user=user.id).first()

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
		# "user_description": user.usertype,
		"token": token,
		"user": user.id,
		"username": user.username,
		"email": user.email,
		"superuser" : user.is_superuser,
		'code': 20000,
		"staff": user.is_staff,
		# 'first_name': user.first_name,
		# 'last_name': user.last_name,
		"orig_iat": timezone.now(),
		#"user_braintree_id": UserCheckout.objects.get(user=user).get_braintree_id
	}
	return data
