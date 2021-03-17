from django.urls import path,re_path
from .views import GetSDLdata



app_name = 'address'

urlpatterns = [
	path('', GetSDLdata.as_view(), name="index"),
]
