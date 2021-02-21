
from django.contrib import admin
from django.urls import path
from .import views


# Error Handling 404
# handler404 = views.handler404

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    
]


