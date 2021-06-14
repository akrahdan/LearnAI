from django.urls import path
from .views import subscription, info, paymentMethod, invoice, invoiceDetail

urlpatterns = [
    path('info/', info, name='info' ),
    path('invoice/', invoice, name='invoice' ),
    path('invoice-detail/', invoiceDetail, name='invoice-details' ),
    path('payment/', paymentMethod, name='payment' ),
    path('subscription/', subscription, name='subscription' )
]