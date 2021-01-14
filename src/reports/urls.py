from django.conf.urls import url, re_path, include
from django.urls import include, path

from .views import DailySalesApiView, UserCountProductWiseReport, UserWithoutPurchaseReport, UserOrderDetailReport, SalesAndCreditReportByDeliveryBoy


urlpatterns = [
    re_path('reports-daily/$', DailySalesApiView.as_view(), name='daily_sales_api'),
    
    re_path('UserCountProductWiseReport/$', UserCountProductWiseReport, name='UserCountProductWiseReport'),
    re_path('UserWithoutPurchaseReport/$', UserWithoutPurchaseReport, name='UserWithoutPurchaseReport'),
    re_path('UserOrderDetailReport/$', UserOrderDetailReport, name='UserOrderDetailReport'),
    re_path('api/SalesAndCreditReportByDeliveryBoy/$', SalesAndCreditReportByDeliveryBoy.as_view(), name='SalesAndCreditReportByDeliveryBoy'),
    
    ]


    