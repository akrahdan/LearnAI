from django.db import models

# Create your models here.
import math
import datetime
from django.conf import settings
from django.db import models
from django.db.models import Count, Sum, Avg
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils import timezone

from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from readux.db.utils import unique_purchase_id_generator
from courses.models import Course



class PurchaseStatusChoices(models.TextChoices):
    CREATED = 'created', 'Created'
    PAID = 'paid', 'Paid'
    REFUNDED = 'refunded', 'Refunded'

class PurchaseManagerQuerySet(models.query.QuerySet):
    def recent(self):
        return self.order_by("-updated", "-timestamp")

    def get_sales_breakdown(self):
        recent = self.recent().not_refunded()
        recent_data = recent.totals_data()
        recent_cart_data = recent.cart_data()
        paid = recent.by_status(status='paid')
        paid_data = paid.totals_data()
        data = {
            'recent': recent,
            'recent_data':recent_data,
            'recent_cart_data': recent_cart_data,
            'paid': paid,
            'paid_data': paid_data
        }
        return data

    def by_weeks_range(self, weeks_ago=7, number_of_weeks=2):
        if number_of_weeks > weeks_ago:
            number_of_weeks = weeks_ago
        days_ago_start = weeks_ago * 7  # days_ago_start = 49
        days_ago_end = days_ago_start - (number_of_weeks * 7) #days_ago_end = 49 - 14 = 35
        start_date = timezone.now() - datetime.timedelta(days=days_ago_start)
        end_date = timezone.now() - datetime.timedelta(days=days_ago_end) 
        return self.by_range(start_date, end_date=end_date)

    def by_range(self, start_date, end_date=None):
        if end_date is None:
            return self.filter(updated__gte=start_date)
        return self.filter(updated__gte=start_date).filter(updated__lte=end_date)

    def by_date(self):
        now = timezone.now() - datetime.timedelta(days=9)
        return self.filter(updated__day__gte=now.day)

    def totals_data(self):
        return self.aggregate(Sum("total"), Avg("total"))

    def cart_data(self):
        return self.aggregate(
                        Sum("cart__courses__price"), 
                        Avg("cart__courses__price"), 
                        Count("cart__courses")
                                    )

    def by_status(self, status="paid"):
        return self.filter(status=status)

    def not_refunded(self):
        return self.exclude(status='refunded')

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)

    def not_created(self):
        return self.exclude(status='created')

class PurchaseManager(models.Manager):
    def get_queryset(self):
        return PurchaseManagerQuerySet(self.model, using=self._db)

    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
                billing_profile=billing_profile, 
                cart=cart_obj, 
                active=True, 
                status='created'
            )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    billing_profile=billing_profile, 
                    cart=cart_obj)
            created = True
        return obj, created



# Random, Unique
class Purchase(models.Model):
    billing_profile     = models.ForeignKey(BillingProfile, null=True, blank=True, on_delete=models.SET_NULL)
    purchase_id            = models.CharField(max_length=120, blank=True) # AB31DE3
    billing_address     = models.ForeignKey(Address, related_name="billing_address", null=True, blank=True, on_delete=models.SET_NULL)
    billing_address_final     = models.TextField(blank=True, null=True)
    cart                = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status              = models.CharField(max_length=120, default=PurchaseStatusChoices.CREATED, choices=PurchaseStatusChoices.choices)
    total               = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    active              = models.BooleanField(default=True)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.purchase_id

    objects = PurchaseManager()

    class Meta:
       ordering = ['-timestamp', '-updated']

    def get_absolute_url(self):
        return reverse("purchases:detail", kwargs={'purchase_id': self.purchase_id})

    def get_status(self):
        if self.status == "refunded":
            return "Refunded purchase"
      

    def update_total(self):
        cart_total = self.cart.total
        formatted_total = format(cart_total, '.2f')
        self.total = formatted_total
        self.save()
        return cart_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        total   = self.total
        if billing_profile and billing_address and total > 0:
            return True
        return False

    def update_purchases(self):
        for p in self.cart.courses.all():
            obj, created = CoursePurchase.objects.get_or_create(
                    purchase_id=self.purchase_id,
                    product=p,
                    billing_profile=self.billing_profile
                )
        return CoursePurchase.objects.filter(purchase_id=self.purchase_id).count()

    def mark_paid(self):
        if self.status != 'paid':
            if self.check_done():
                self.status = "paid"
                self.save()
                self.update_purchases()
        return self.status


def pre_save_create_purchase_id(sender, instance, *args, **kwargs):
    if not instance.purchase_id:
        instance.purchase_id = unique_purchase_id_generator(instance)
    qs = Purchase.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    if qs.exists():
        qs.update(active=False)


    if instance.billing_address and not instance.billing_address_final:
        instance.billing_address_final = instance.billing_address.get_address()


pre_save.connect(pre_save_create_purchase_id, sender=Purchase)


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Purchase.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            purchase_obj = qs.first()
            purchase_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)


def post_save_purchase(sender, instance, created, *args, **kwargs):
    #print("running")
    if created:
        print("Updating... first")
        instance.update_total()


post_save.connect(post_save_purchase, sender=Purchase)



class CoursePurchaseQuerySet(models.query.QuerySet):
    def active(self):
        return self.filter(refunded=False)

    def by_request(self, request):
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        return self.filter(billing_profile=billing_profile)



class CoursePurchaseManager(models.Manager):
    def get_queryset(self):
        return CoursePurchaseQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()


    def by_request(self, request):
        return self.get_queryset().by_request(request)

    def course_by_id(self, request):
        qs = self.by_request(request)
        ids_ = [x.course.id for x in qs]
        return ids_

    def courses_by_request(self, request):
        ids_ = self.course_by_id(request)
        courses_qs = Course.objects.filter(id__in=ids_).distinct()
        return courses_qs



class CoursePurchase(models.Model):
    purchase_id            = models.CharField(max_length=120)
    billing_profile     = models.ForeignKey(BillingProfile, on_delete=models.CASCADE) # billingprofile.productpurchase_set.all()
    course             = models.ForeignKey(Course, on_delete=models.CASCADE) # product.productpurchase_set.count()
    refunded            = models.BooleanField(default=False)
    updated             = models.DateTimeField(auto_now=True)
    timestamp           = models.DateTimeField(auto_now_add=True)

    objects = CoursePurchaseManager()

    def __str__(self):
        return self.product.title





