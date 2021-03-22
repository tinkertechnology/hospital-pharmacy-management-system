from django.contrib import admin

# Register your models here.
from .models import Country, District, State, LocalGov

admin.site.register(Country)
admin.site.register(State)
admin.site.register(District)
admin.site.register(LocalGov)

