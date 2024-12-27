from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_now, name='book_now'),  
    path('contact/submit/', views.contact_submit, name='contact_submit'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    path('get-disabled-dates/', views.get_disabled_dates, name='get_disabled_dates'),
]
