from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect


from addresses.models import Address

from billing.models import BillingProfile
from orders.models import Order
from courses.models import Course
from .models import Cart




def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    courses = [{
            "id": x.id,
            "url": x.get_absolute_url(),
            "name": x.name, 
            "price": x.price
            } 
            for x in cart_obj.courses.all()]
    cart_data  = {"courses": courses, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)

def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, "carts/home.html", {"cart": cart_obj})


def cart_update(request):
    course_id = request.POST.get('course_id')
    
    if course_id is not None:
        try:
            course_obj = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            print("Show message to user, course is gone?")
            return redirect("cart_home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if course_obj in cart_obj.courses.all():
            cart_obj.courses.remove(course_obj)
            added = False
        else:
            cart_obj.courses.add(course_obj) # cart_obj.courses.add(course_id)
            added = True
        request.session['cart_items'] = cart_obj.courses.count()
        # return redirect(course_obj.get_absolute_url())
        if request.is_ajax(): # Asynchronous JavaScript And XML / JSON
            print("Ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.courses.count()
            }
            return JsonResponse(json_data, status=200) # HttpResponse
            # return JsonResponse({"message": "Error 400"}, status=400) # Django Rest Framework
    return redirect("cart_home")



def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.courses.count() == 0:
        return redirect("cart_home")  
    
    billing_address_id = request.session.get("billing_address_id", None)



    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
       
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id) 
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
                order_obj.mark_paid() # sort a signal for us
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







def checkout_done_view(request):
    return render(request, "carts/checkout-done.html", {})






