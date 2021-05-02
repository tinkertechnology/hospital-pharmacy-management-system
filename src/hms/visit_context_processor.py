
from account.models import Visit
from datetime import datetime, timedelta, time
from rest_framework.response import Response
from django.utils import timezone

def opd_auto_checkout(request):
    # return {}
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())

    visit_type_to_filter = 'OPD'
    # filter_opd_visit = Visit.objects.filter(fk_visit__slug='OPD', timestamp__lte=today_end, timestamp__gte=today_start)
    filter_opd_visit = Visit.objects.filter(fk_visit__slug='OPD', timestamp__gte=timezone.now().replace(hour=0, minute=0, second=0), timestamp__lte=timezone.now().replace(hour=23, minute=59, second=59))
    print('filter00', filter_opd_visit)
    if filter_opd_visit:  
        print('noob')      
        for opd_visit in filter_opd_visit:
            opd_visit.visit_status = True
            opd_visit.save()
        # return Response('visits_has_been_checkout', status=200)
        print('visits_has_been_checkout')
        return {}
    else:
        print('no visits')
        
        return {}

            
