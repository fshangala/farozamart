from django.urls import path
from paymentgateway import views

app_name='paymentgateway'
urlpatterns = [
    path('payment-methods/',views.PaymentMethods.as_view(),name='payment-methods'),
    path('cod-pwyment/',views.CODPayment.as_view(),name='cod-payment'),
]
