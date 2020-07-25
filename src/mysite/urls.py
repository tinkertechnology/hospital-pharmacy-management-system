"""mysite re_path Configuration

The `re_pathpatterns` list routes re_paths to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/re_paths/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a re_path to re_pathpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a re_path to re_pathpatterns:  path('', Home.as_view(), name='home')
Including another re_pathconf
    1. Import the include() function: from django.re_paths import include, path
    2. Add a re_path to re_pathpatterns:  path('blog/', include('blog.re_paths'))
"""
from django.contrib import admin
from django.conf.urls import url, re_path, include
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.conf import settings

from personal.views import (
	home_screen_view, dashboard_view
)
# from sarovara_web import urls as sarovara_urls

from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    privacy_policy,
    account_jpt,
	must_authenticate_view,
    ValidatePhoneSendOTP,
    ValidateOTP,
    RegisterAPI,
    ResetPasswordAPIView,
    ChangePasswordAPIView,
    PasswordResetSendOTP,
    ValidateResetPasswordOTP,
    ChangePasswordAfterOtpAPIView

)





from carts.views import (
        CartAPIView,
        CartView, 
        CheckoutAPIView,
        CheckoutFinalizeAPIView,
        CheckoutView, 
        CheckoutFinalView,
        ItemCountView, 
        AddToCartView,
        RemoveCartItemFromCart

        )
from orders.views import (
                    AddressSelectFormView, 
                    UserAddressCreateView,
                    AccountsVerifyRegistrationView,
                    AccountsResetPasswordView,
                    UserAddressCreateAPIView,
                    UserAddressListAPIView,
                    UserCheckoutAPI,
                    OrderList,
                    OrderListAPIView, 
                    OrderDetail,
                    OrderRetrieveAPIView,
                    SendQuotationApiView,
                    CartOrderApiView, 
                    UserOrderView,
                    UserOrderDetailView,
                    OrderLists,
                    OrderHistoryLists,
                    CartOrderLists,
                    StoreWiseCartOrderLists,
                    UpdateOrderStatusApiView,
                    StoreWiseOrderHistoryLists,
                    UpdateStoreWiseOrderStatusApiView,

                    StoreWiseOrderLists,
                    myStoreName
                    )

from products.views import (
        APIHomeView,
        CategoryListAPIView,
        CategoryRetrieveAPIView,
        ProductListAPIView,
        ProductRetrieveAPIView,
        ProductFeaturedListAPIView,
        CompanyListAPIView,
        BrandListAPIView,
        GenericNameListAPIView,
        ProductUnitListAPIView,
        WSCListAPIView,
        WSCRetrieveAPIView,
        CreateProductAPIView,
        CommonProductListAPIView,
        AddProductAPIView,
        AllProductListAPIView,
        AllProductRetrieveAPIView,
        ProductVariationRetrieveAPIView
        

    )

from prescription.views import(


    ApiPostFile
    )

from inquiry.views import (
    InquiryApiView,
    message_list,
    view_messages

    )

from users.views import (
    UserInquiryList,
    UserInquiryForPharmacist
    
    )



#API Patterns
urlpatterns = [
    url(r'^accounts/', include('rest_registration.api.urls')),
    url('', include('reports.urls')),

    re_path(r'^api/$', APIHomeView.as_view(), name='home_api'),
    re_path(r'^api/validate_mobile/', ValidatePhoneSendOTP.as_view(), name="validate_mobile"),
    re_path(r'^api/validate_otp/', ValidateOTP.as_view(), name="validate_otp"),
    re_path(r'^api/register/', RegisterAPI.as_view(), name="register"),
    re_path(r'^api/reset_password/', ResetPasswordAPIView.as_view(), name="reset_password"),
    re_path(r'^api/reset_password_otp/', PasswordResetSendOTP.as_view(), name="reset_password_otp"),
    re_path(r'^api/validate_reset_password_otp/', ValidateResetPasswordOTP.as_view(), name="validate_reset_password_otp"),
    re_path(r'^api/change_password_afterotp/', ChangePasswordAfterOtpAPIView.as_view(), name="change_password_afterotp"),
    re_path(r'^api/change_password/', ChangePasswordAPIView.as_view(), name="change_password"),
    re_path(r'^api/file_upload/$', ApiPostFile.as_view(), name='file_upload'),

    
    # re_path(r'^api/upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    # re_path(r'^api/upload/$', FileUploadView.as_view()),


    re_path(r'^api/cart/$', CartAPIView.as_view(), name='cart_api'),
    re_path(r'^api/checkout/$', CheckoutAPIView.as_view(), name='checkout_api'),
    re_path(r'^api/checkout/finalize/$', CheckoutFinalizeAPIView.as_view(), name='checkout_finalize_api'),
    re_path(r'^api/auth/token/$', obtain_jwt_token, name='auth_login_api'),
    re_path(r'^api/auth/token/refresh/$', refresh_jwt_token, name='refresh_token_api'),
    re_path(r'^api/user/address/$', UserAddressListAPIView.as_view(), name='user_address_list_api'),
    re_path(r'^api/user/address/create/$', UserAddressCreateAPIView.as_view(), name='user_address_create_api'),
    re_path(r'^api/user/checkout/$', UserCheckoutAPI.as_view(), name='user_checkout_api'),
    re_path(r'^api/categories/$', CategoryListAPIView.as_view(), name='categories_api'),
    re_path(r'^api/categories/(?P<pk>\d+)/$', CategoryRetrieveAPIView.as_view(), name='category_detail_api'),

    re_path(r'^api/wscs/$', WSCListAPIView.as_view(), name='wscs_api'),
    re_path(r'^api/wscs/(?P<pk>\d+)/$', WSCRetrieveAPIView.as_view(), name='wscs_detail_api'),
    re_path(r'^api/orders/$', OrderListAPIView.as_view(), name='orders_api'),


    re_path(r'^api/store_orders/$', OrderLists.as_view(), name='orders_store'), ##for_customer
    

    re_path(r'^api/orders_lists/$', CartOrderLists.as_view(), name='orders_lists'), ###uptech_

    re_path(r'^api/storewise_orders/$', StoreWiseOrderLists.as_view(), name='storewise_orders_store'),
    re_path(r'^api/storewise_orders_lists/$', StoreWiseCartOrderLists.as_view(), name='storewise_orders_lists'),
    re_path(r'^api/storewise_orders_history_lists/$', StoreWiseOrderHistoryLists.as_view(), name='storewise_orders_history_lists'),
    re_path(r'^api/store_name/$', myStoreName.as_view(), name='store_name'),

    

    re_path(r'^api/orders_status/$', UpdateOrderStatusApiView.as_view(), name='orders_status_update'), ##pharms

    re_path(r'^api/storwise_change_orders_status/$', UpdateStoreWiseOrderStatusApiView.as_view(), name='storewise_orders_status_update'),


    re_path(r'^api/orders_history/$', OrderHistoryLists.as_view(), name='orders_history'),
    
    re_path(r'^api/orders/(?P<pk>\d+)/$', OrderRetrieveAPIView.as_view(), name='order_detail_api'),
    re_path(r'^api/products/$', ProductListAPIView.as_view(), name='products_api'),
    re_path(r'^api/ProductVariationRetrive/(?P<pk>\d+)/$', ProductVariationRetrieveAPIView.as_view(), name='ProductVariationRetriveApiView'),
    re_path(r'^api/all_products/$', AllProductListAPIView.as_view(), name='all_products_api'), ## for pharma
    
    
    re_path(r'^api/products_create/$', CreateProductAPIView.as_view(), name='products_create_api'),
    re_path(r'^api/products_add/$', AddProductAPIView.as_view(), name='products_create_api'), ##pharmas
    
    re_path(r'^api/products_common/$', CommonProductListAPIView.as_view(), name='products_common_api'),

    re_path(r'^api/products/(?P<pk>\d+)/$', ProductRetrieveAPIView.as_view(), name='products_detail_api'),
    re_path(r'^api/all_products/(?P<pk>\d+)/$', AllProductRetrieveAPIView.as_view(), name='all_products_detail_api'),##Pharmas

    re_path(r'^api/quotation/$', SendQuotationApiView.as_view(), name="send_quotation_api"),
    re_path(r'^api/featured/$', ProductFeaturedListAPIView.as_view(), name='product_featured_api'),
    re_path(r'^api/create_cart/$', AddToCartView.as_view(), name="create_cart_api"),
    re_path(r'^api/delete_cart_item/(?P<pk>\d+)/$', RemoveCartItemFromCart.as_view(), name="delete_cart_item"),
    re_path(r'^api/create_order/$', CartOrderApiView.as_view(), name="create_order_api"),
    re_path(r'^api/companies/$', CompanyListAPIView.as_view(), name="company_list_api"),
    re_path(r'^api/brands/$', BrandListAPIView.as_view(), name="brands_list_api"),
    re_path(r'^api/generic_names/$', GenericNameListAPIView.as_view(), name="generic_name_list_api"),
    re_path(r'^api/product_units/$', ProductUnitListAPIView.as_view(), name="product_unit_list_api"),    

    ######### Inquiry api #############
    re_path(r'^api/send_inquiry/$', InquiryApiView.as_view(), name="inquiry_api"),
    re_path(r'^api/inquiry_users_list/$', UserInquiryList.as_view(), name="inquiry_user"),
    re_path(r'^api/inquiry_users_pharmacist_list/$', UserInquiryForPharmacist.as_view(), name="inquiry_user_pharmacist"),
    
    re_path(r'^api/messages/(?P<sender>\w+)/(?P<receiver>\w+)/$', message_list, name='message-detail'),
    re_path(r'^api/view_messages/$', view_messages.as_view(), name='view-messages'),


]



from slider.views import(
        SliderListAPIView
    )


urlpatterns += [
    re_path(r'^api/sliders/$', SliderListAPIView.as_view(), name='sliders_api'),
    ]

#Report URLS


# Membership api
from membership.views import (
        MembershipTypeListCreateApiView,
        MembershipTypeRetrieveUpdateDestroyApiView,
        UserMembershipListCreateApiView,
        UserMembershipRetrieveUpdateDestroyApiView,
        UserMembershipRetrieveApiView,
        
)
from membership import views as membership_views
urlpatterns += [
    re_path(r'^api/membership-type/$', MembershipTypeListCreateApiView.as_view(), name='api-membership-type'),
    re_path(r'^api/membership-type/(?P<pk>\d+)/$', MembershipTypeRetrieveUpdateDestroyApiView.as_view(), name='api-membership-type'),
    re_path(r'^api/user-membership/$', UserMembershipListCreateApiView.as_view(), name='api-user-membership'),
    re_path(r'^api/user-membership/(?P<pk>\d+)/$', UserMembershipRetrieveUpdateDestroyApiView.as_view(), name='api-membership-type'),
    re_path(r'^api/user-membership-retrieve/$', UserMembershipRetrieveApiView.as_view(), name='api-user-membership-retrieve'),
    re_path(r'^api/user_membership_auto_order/$', membership_views.UserMembershipAutoOrderListCreateApiView.as_view(), name='api-user-membership-retrieve'),
    re_path(r'^api/user_membership_user_auto_orders_list/$', membership_views.UserMembershipUserAutoOrdersListApiView.as_view(), name='api-user-membership-auto-order-list'),
]

# store api
from store.views import (
        StoreListCreateApiView,
        StoreRetrieveUpdateDestroyApiView,
        ListCompaniesApiView,
        StoreDeliverUserList,
        ChangeDeliveryUserRoute
)
urlpatterns += [
    re_path(r'^api/store/$', StoreListCreateApiView.as_view(), name='api-store'),
    re_path(r'^api/store/(?P<pk>\d+)/$', StoreRetrieveUpdateDestroyApiView.as_view(), name='api-store-retrieve'),
    re_path(r'^api/stores/$', ListCompaniesApiView.as_view(), name='api-stores-list'),
    re_path(r'^api/store-delivery-users-list/$', StoreDeliverUserList.as_view(), name='delivery-users-list'),
    re_path(r'^api/store-user-change-route/$', ChangeDeliveryUserRoute.as_view(), name='store-user-change-route'),
    
]

# store api
from payment.views import (
        PaymentMethodListCreateApiView,
        PaymentMethodRetrieveUpdateDestroyApiView,
)
urlpatterns += [
    re_path(r'^api/paymentmethod/$', PaymentMethodListCreateApiView.as_view(), name='api-paymentmethod'),
    re_path(r'^api/paymentmethod/(?P<pk>\d+)/$', PaymentMethodRetrieveUpdateDestroyApiView.as_view(), name='api-paymentmethod-retrieve'),
]

# esewa payment
from payment_esewa import views as payment_esewa_views
urlpatterns += [
    path('payment/payment_esewa_confirm',payment_esewa_views.payment_esewa_confirm),
    path('payment/payment_esewa_success',payment_esewa_views.payment_esewa_success),
    path('payment/payment_esewa_fail',payment_esewa_views.payment_esewa_fail),
    path('payment/payment-esewa-app-request', payment_esewa_views.payment_esewa_app_request)
]

# routes
from routes import views as routes_views
urlpatterns += [
    re_path(r'^api/route/$', routes_views.RouteListCreateApiView.as_view(), name='api-route'),
    re_path(r'^api/route/(?P<pk>\d+)/$', routes_views.RouteRetrieveUpdateDestroyApiView.as_view(), name='api-route-retrieve'),

    re_path(r'^api/routedetail/$', routes_views.RouteDetailListCreateApiView.as_view(), name='api-routedetail'),
    re_path(r'^api/routedetail/(?P<pk>\d+)/$', routes_views.RouteDetailRetrieveUpdateDestroyApiView.as_view(), name='api-routedetail-retrieve'),
    re_path(r'^api/storewise_route/$', routes_views.StoreWiseRouteListApiView.as_view(), name='api-storewise_routedetail'),
    

    path('route_detail_view',routes_views.route_detail_view),
]


from sarovara_web import views
handler404 = views.handler404

urlpatterns += [
 
    # re_path(r'^$', newsletter_views.home, name='home'),
    # re_path(r'^contact/$', newsletter_views.contact, name='contact'),
    # re_path(r'^about/$', ecommerce2_views.about, name='about'),
    # # re_path(r'^blog/', include('blog.re_paths'))

 
    # # re_path(r'^accounts/', include('registration.backends.default.re_paths')),
    # re_path(r'^products/', include('products.re_paths')),
    # re_path(r'^accounts/', include('rest_registration.api.re_paths')),
    
    # re_path(r'^categories/', include('products.re_paths_categories')),
    # re_path(r'^orders/$', OrderList.as_view(), name='orders'),
    # re_path(r'^orders/(?P<pk>\d+)/$', OrderDetail.as_view(), name='order_detail'),
    # re_path(r'^cart/$', CartView.as_view(), name='cart'),
    # re_path(r'^cart/count/$', ItemCountView.as_view(), name='item_count'),
    # re_path(r'^checkout/$', CheckoutView.as_view(), name='checkout'),
    # re_path(r'^checkout/address/$', AddressSelectFormView.as_view(), name='order_address'),
    # re_path(r'^checkout/address/add/$', UserAddressCreateView.as_view(), name='user_address_create'),
    # re_path(r'^checkout/final/$', CheckoutFinalView.as_view(), name='checkout_final'),
    # re_path(r'^accounts-verify-registration/$', AccountsVerifyRegistrationView),
    # re_path(r'^accounts-reset-password/$', AccountsResetPasswordView),

    # re_path(r'^api/v1/', include(re_pathpatterns)),
    # re_path(r'^rest-auth/registration/', include('rest_auth.registration.re_paths')),
    # re_path(r'^account/', include('allauth.re_paths')),
    # re_path(r'^logout/$', TemplateView.as_view(template_name="logout.html")),
    # re_path(r'^rest-auth/', include('rest_auth.re_paths')),
    # re_path(r'^password-reset/$',TemplateView.as_view(template_name="password_reset.html"),name='password-reset'),
    # re_path(r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     TemplateView.as_view(template_name="password_reset_confirm.html"),
    #     name='password_reset_confirm'),


]









urlpatterns += [
    path(r'admin/', admin.site.urls),
    path('', include('sarovara_web.urls')),
    # path('', home_screen_view, name="home"),
    path('dashboard', dashboard_view, name="dashboard"),
    path('account/', account_view, name="account"),
    path('blog/', include('blog.urls', 'blog')),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('privacy-policy/', privacy_policy, name="privacy_policy"),
	path('must_authenticate/', must_authenticate_view, name="must_authenticate"),
    path('register/', registration_view, name="register"),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
        name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
        name='password_change'),

    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
     name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
     name='password_reset_complete'),

    path('user_order', UserOrderView, name='user_order'),
    path('user_order_detail/<int:id>/', UserOrderDetailView, name='user_order_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
