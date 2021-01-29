from django.urls import path
from .views import AppSettingsAPIView, MobileAppVersion, JptEchoTest

app_name = 'app_settings'

urlpatterns = [
    path('api/AppSettings/JptEchoTest', JptEchoTest.as_view(), name="api-appsettings-jptechotest"),
    path('api/AppSettings/', AppSettingsAPIView.as_view(), name="api-appsettingsget"),
    path('api/MobileAppVersion/', MobileAppVersion.as_view(), name="api-mobileappversion"),
 ]
