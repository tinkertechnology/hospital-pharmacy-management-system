from django.conf import settings

from .models import CallLog
from datetime import datetime

#staff enters order of client, who gave missed call
def ServiceCallLogStaffEntryOrder(data):
	settings.DLFPRINT()
	number = data.get('number');
	q = CallLog.objects.filter(staff_entry_at=None)
	calllogs = q.all()
	for calllog in calllogs:
		calllog.staff_entry_at = datetime.now()
		calllog.save()
	return
	