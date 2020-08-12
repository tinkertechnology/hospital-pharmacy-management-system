# python manage.py shell < "E:\job\cp\kua_water_app\test_shell.py"
# python manage.py shell < membershipAutoOrder.py
# from membership.service import StartUserMembershipAutoOrder

import membership.service as ms
ms.StartUserMembershipAutoOrder()

exit()