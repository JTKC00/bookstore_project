import stripe
from django.conf import settings
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order, OrderItem

stripe.api_key = settings.STRIPE_SECRET_KEY

class PaymentPageView(View):
    def get(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id, userId=request.user)
        order_items = OrderItem.objects.filter(orderid=order)
        order_total = order.total_amount
        return render(request, 'payments/payment.html', {
            'order': order,
            'order_items': order_items,
            'order_total': order_total,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
        })

class CreateCheckoutSessionView(View):
    def post(self, request, order_id, *args, **kwargs):
        order = get_object_or_404(Order, id=order_id, userId=request.user)
        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'hkd',
                            'product_data': {
                                'name': f'訂單 #{order.id}',
                            },
                            'unit_amount': int(order.total_amount * 100),  # Stripe 以分為單位
                        },
                        'quantity': 1,
                    }
                ],
                mode='payment',
                success_url=request.build_absolute_uri('/payments/success/'),
                cancel_url=request.build_absolute_uri('/payments/cancel/'),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import stripe

@csrf_exempt
def stripe_webhook(request):
    if request.method == 'POST':
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = 'your_signing_secret'  # 從 Stripe Dashboard 獲取

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except ValueError as e:
            return HttpResponse(f"Error: {str(e)}", status=400)
        except stripe.error.SignatureVerificationError as e:
            return HttpResponse(f"Error: {str(e)}", status=400)

        if event['type'] == 'charge.succeeded':
            print(f"Received charge.succeeded event: {event['data']['object']['id']}")
            return HttpResponse("Webhook received", status=200)

        return HttpResponse("Unhandled event", status=200)
    elif request.method == 'GET':
        return HttpResponse("Webhook endpoint is active", status=200)
    return HttpResponse("Method not allowed", status=405)

def fps_payment(request):
    if request.method == "POST":
        # 這裡可以處理 FPS 付款資料，例如上傳收據
        return render(request, 'payments/success.html', {'method': 'FPS'})
    return redirect('payments:payment')

def paypal_payment(request):
    if request.method == "POST":
        # 這裡可以處理 PayPal 付款資料
        return render(request, 'payments/success.html', {'method': 'PayPal'})
    return redirect('payments:payment')

def payment_success(request):
    return render(request, 'payments/success.html')

def payment_cancel(request):
    return render(request, 'payments/cancel.html')