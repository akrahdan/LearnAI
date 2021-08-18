
import json
from django.shortcuts import render
from django.views.generic import View
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
from .serializers import CreateOrderSerializer, ProjectOrderSerializer


class CompleteOrderView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        if request.data is None:
            return Response({'detail': 'Error'}, status=status.HTTP_403_FORBIDDEN)
        resp = CaptureOrder().capture_order(order_id=request.data.get('orderID'))

        billingProfile, profile_created = BillingProfile.objects.get_or_create(
            user=user,
            full_name=resp.result.purchase_units[0].shipping.name.full_name,
            email=resp.result.payer.email_address
        )

        billingAddress, address_created = Address.objects.get_or_create(
            billing_profile=billingProfile,
            address_line_1=resp.result.purchase_units[0].shipping.address.address_line_1,
            address_line_2=resp.result.purchase_units[0].shipping.address.admin_area_2,
            postal_code=resp.result.purchase_units[0].shipping.address.postal_code,
            country_code=resp.result.purchase_units[0].shipping.address.country_code
        )

        order = Order.objects.create(
            billing_profile=billingProfile,
            address=billingAddress,
            total=resp.result.purchase_units[0].payments.captures[0].amount.value,

        )
        serializer = CreateOrderSerializer(instance=order)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class VerifyOwnership(View):
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            data = request.GET
            project_id = request.GET.get('project_id', None)
            if project_id is not None:
                project_id = int(project_id)
                ownership_ids = ProjectOrder.objects.projects_by_id(request)
                if project_id in ownership_ids:
                    return JsonResponse({'owner': True})
            return JsonResponse({'owner': False})
        raise Http404


class MyProjectsView(APIView):
    authentication_classes = [authentication.TokenAuthentication,
                              authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):

        billing_qs = BillingProfile.objects.filter(user=request.user)
        if billing_qs.exists():
            project_qs = ProjectOrder.objects.filter(
                billing_profile=billing_qs.first())
            if project_qs.exists():
                serializer = ProjectOrderSerializer(project_qs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({'detail': 'No project associated with your profile'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'detail': 'No billing profile associated with your account'}, status=status.HTTP_400_BAD_REQUEST)
