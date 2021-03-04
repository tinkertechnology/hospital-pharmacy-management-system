from django.urls import path,re_path
from .import views



app_name = 'vendor'

urlpatterns = [
	path('', views.index, name="index"),
	path('add/', views.add, name="add"),
	path('<int:id>/edit/',  views.edit, name='edit'),
	path('<int:id>/delete/', views.delete, name='delete'),
]
