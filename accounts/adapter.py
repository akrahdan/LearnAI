from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from carts.models import Cart
class AccountAdapter(DefaultAccountAdapter):

    def get_login_redirect_url(self, request):
        cart, created = Cart.objects.new_or_get(request)
        if created or cart.courses.count() == 0:
          return super().get_login_redirect_url(request)
        return '/cart'