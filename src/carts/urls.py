from django.urls import path
from courses.views import CourseCheckoutView
from .views import (
    cart_home,
    checkout_done_view,
    checkout_home,
    CheckoutView,
    CheckoutPayView,
    cart_update
)
urlpatterns = [
    path('checkout/course/<slug:slug>/', CourseCheckoutView.as_view(), name='checkout'),
    path('', cart_home, name='cart_home'),
    path('checkout/success/', checkout_done_view, name='cart_success'),
    path('checkout/', CheckoutView.as_view(), name='cart_checkout'),
    path('api/checkout/', CheckoutPayView.as_view(), name='cart_checkout_api'),
    path('checkout/done', checkout_done_view, name='checkout_done'),
    path('update/', cart_update, name='cart_update'),

]