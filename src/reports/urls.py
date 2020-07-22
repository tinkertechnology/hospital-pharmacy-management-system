from django.conf.urls import url, re_path, include
from django.urls import include, path

from .views import DailySalesApiView


urlpatterns = [
    re_path(r'^api/reports-daily/$', DailySalesApiView.as_view(), name='daily_sales_api'),
    ]