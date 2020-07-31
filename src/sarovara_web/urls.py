
from django.contrib import admin
from django.urls import path
from .import views


# Error Handling 404
handler404 = views.handler404

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('we-sales', views.we_sales, name='we-sales'),
    path('our-depot', views.our_depot, name='our-depot'),
    path('about-us', views.about_us, name='about-us'),
    path('contacts', views.contacts, name='contacts'),
    path('terms-and-conditions', views.terms_and_condition, name='terms-and-conditions'),
    path('privacy-policy', views.privacy_policy, name='privacy-policy'),
    path('buy-drinking-water', views.buy_drinking_water, name='buy-drinking-water'),
    path('sell-drinking-water', views.sell_drinking_water, name='sell-drinking-water'),
    path('open-depot', views.open_depot, name='open-depot'),
    path('feedback', views.feedback, name='feedback'),
    path('complaint', views.complaint, name='complaint'),
    path('careers', views.careers, name='careers'),
    path('careers/vacancy-apply-now', views.vacancy_apply_now, name='vacancy-apply-now'),
    path('kuwa-drinking-water', views.kuwa_drinking_water, name='kuwa-drinking-water'),
    path('karuwa-premium-drinking-water', views.karuwa_premium_drinking_water, name='karuwa-premium-drinking-water'),
    path('patanjali-dibyajal', views.patanjali_dibyajal, name='patanjali-dibyajal'),

    # path('success', views.success, name='success'),
    path('buy-drinking-water', views.buy_drinking_water, name='buy-drinking-water'),
    path('request-open-depot', views.request_open_depot, name='request-open-depot'),
    path('request-feedback', views.request_feedback, name='request-feedback'),
    path('request-complaint', views.request_complaint, name='request-complaint'),
    path('apply-vacancy-now', views.apply_vacancy_now, name='apply-vacancy-now'),
]


