from django.urls import include, path
from . import views
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.ipn.views import ipn

urlpatterns = [
    path('', views.home, name='home'),  
    path('book/', views.book_now, name='book_now'),
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('get-disabled-dates/', views.get_disabled_dates, name='get_disabled_dates'),
    path('privacy-policy/', TemplateView.as_view(template_name="privacy_policy.html"), name='privacy_policy'),
    path('data-request/', views.data_request_view, name='data_request'),
    path('booking/payment/<int:booking_id>/', views.booking_payment, name='booking_payment'),
    path('paypal/', csrf_exempt(ipn), name='paypal-ipn'),  # Handles both
    path('paypal/ipn/', csrf_exempt(ipn)),  # Explicitly for /paypal/ipn/
]
