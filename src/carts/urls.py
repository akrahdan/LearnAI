from django.urls import path
from courses.views import CourseCheckoutView
from .views import (
    cart_home,
    checkout_done_view,
    checkout_home,
    cart_update
)
urlpatterns = [
    path('checkout/course/<slug:slug>/', CourseCheckoutView.as_view(), name='checkout'),
    path('', cart_home, name='cart_home'),
    path('checkout/success/', checkout_done_view, name='cart_success'),
    path('checkout/$', checkout_home, name='cart_checkout'),
    path('update/', cart_update, name='cart_update'),

]