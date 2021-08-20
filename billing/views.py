from django.shortcuts import render

# Create your views here.

def subscription(request):
    return render(request, 'students/subscriptions.html')

def invoice(request):
    return render(request, 'students/invoice.html')

def invoiceDetail(request):
    return render(request, 'students/invoice-details.html')

def info(request):
    return render(request, 'students/billing-info.html')

def paymentMethod(request):
    return render(request, 'students/payment-method.html')

