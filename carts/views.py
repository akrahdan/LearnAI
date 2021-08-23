from os import error
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from rave_python.rave_exceptions import TransactionVerificationError
from rest_framework.views import APIView

from rave_python import Rave, RaveExceptions

from addresses.models import Address

from billing.models import BillingProfile
from orders.models import Order
from projects.models import Project
from .models import Cart

from django.http import Http404, JsonResponse
from rest_framework import authentication, permissions, serializers, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from addresses.models import Address
from billing.models import BillingProfile
from orders.models import Order, ProjectOrder
from orders.payments.order import CaptureOrder
from orders.payments.paypal import PayPalClient

from orders.serializers import CreateOrderSerializer


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    projects = [{
        "id": x.id,
        "url": x.get_absolute_url(),
        "name": x.name,
        "price": x.price
    }
        for x in cart_obj.projects.all()]
    cart_data = {"projects": projects,
                 "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    project_id = request.POST.get('project_id')

    if project_id is not None:
        try:
            project_obj = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            print("Show message to user, project is gone?")
            return redirect("cart_home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if project_obj in cart_obj.projects.all():
            cart_obj.projects.remove(project_obj)
            added = False
        else:
            # cart_obj.projects.add(project_id)
            cart_obj.projects.add(project_obj)
            added = True
        request.session['cart_items'] = cart_obj.projects.count()
        # return redirect(project_obj.get_absolute_url())
        if request.is_ajax():  # Asynchronous JavaScript And XML / JSON
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.projects.count()
            }
            return JsonResponse(json_data, status=200)  # HttpResponse
            # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
    return redirect("cart_home")


class CartUpdateView(APIView):
    authentication_classes = [authentication.SessionAuthentication,
                              authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        project_id = request.data.get('project_id')
        if project_id is not None:
            try:
                project_obj = Project.objects.get(id=project_id)
            except Project.DoesNotExist:
                return Response({'detail': 'Project does not exist'}, status=status.HTTP_404_NOT_FOUND)

            cart_obj, new_obj = Cart.objects.new_or_get(request)
            if project_obj in cart_obj.projects.all():
                cart_obj.projects.remove(project_obj)
                added = False
            else:
                # cart_obj.projects.add(project_id)
                cart_obj.projects.add(project_obj)
                added = True
            # request.session['cart_items'] = cart_obj.projects.count()
            return Response({'detail': { 'added': added, 'cart_id': cart_obj.id }}, status=status.HTTP_201_CREATED)
        return Response({'detail': 'Project id was not supplied'}, status=status.HTTP_400_BAD_REQUEST)


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.projects.count() == 0:
        return redirect("cart_home")

    billing_address_id = request.session.get("billing_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
        request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(
                billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(
            billing_profile, cart_obj)

        if billing_address_id:
            order_obj.address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if billing_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST":
        "check that order is done"
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge, crg_msg = billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()  # sort a signal for us
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    '''
                    is this the best spot?
                    '''
                    billing_profile.set_cards_inactive()
                return redirect("cart_success")
            else:
                print(crg_msg)
                return redirect("cart_checkout")
    context = {
        "object": order_obj,
        "billing_profile": billing_profile,
        "address_qs": address_qs,

    }
    return render(request, "carts/checkout.html", context)


class CheckoutView(DetailView):
    template_name = 'carts/checkout.html'
    model = Cart

    def get_object(self):
        cart_obj, cart_created = Cart.objects.new_or_get(self.request)
        if cart_created:
            return
        return cart_obj


class CheckoutPayView(APIView):
    authentication_classes = [
        authentication.SessionAuthentication, authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        order_obj = None
        if cart_created or cart_obj.projects.count() == 0:
            print("What is happening")
            cart_obj.delete()
            return Response({'detail': 'Error'}, status=status.HTTP_403_FORBIDDEN)

        resp = CaptureOrder().capture_order(order_id=request.data.get('orderID'))
        print("What is Capture")
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            request)

        if billing_profile is not None:
            print("What", billing_profile)

            order_obj, order_obj_created = Order.objects.new_or_get(
                billing_profile, cart_obj)
            print("Order", order_obj)


        order_obj.total = resp.result.purchase_units[0].payments.captures[0].amount.value
        order_obj.save()
        is_prepared = order_obj.check_done()
        order_obj.mark_paid()
        cart_obj.delete()
        serializer = CreateOrderSerializer(instance=order_obj)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class CheckoutFlutterView(APIView):
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(ref, request, format=None):
        cart_obj, cart_created = Cart.objects.new_or_get(request)
        order_obj = None
        if cart_created or cart_obj.projects.count() == 0:
            cart_obj.delete()
            return Response({'detail': 'Error'}, status=status.HTTP_403_FORBIDDEN)

        rave = Rave(settings.RAVE_TEST_PUB_KEY,
                    settings.RAVE_TEST_SECRET_KEY, usingEnv=False)
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(
            request)
        
        try:

            res = rave.Card.verify(request.data["txRef"])
        
        except RaveExceptions.TransactionVerificationError as e:
            return Response(e, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
       
        if res["chargecode"] == '00':
            order_obj, order_obj_created = Order.objects.new_or_get(
                billing_profile, cart_obj)
            order_obj.total = float(res["amount"])
            order_obj.save()
            is_prepared = order_obj.check_done()
            order_obj.mark_paid()
            cart_obj.delete()
            serializer = CreateOrderSerializer(instance=order_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data=res, status=status.HTTP_402_PAYMENT_REQUIRED)


def checkout_done_view(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    cart_obj.delete()
    return render(request, "carts/checkout-done.html", {})
