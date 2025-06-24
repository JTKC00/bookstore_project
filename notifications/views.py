from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailNotification
from django.urls import reverse

def send_payment_success_email(order, payment_method):
    subject = f'Payment Confirmation - Order #{order.id}'
    message = f"""
Dear {order.receipient},

Thank you for your payment! Your order #{order.id} has been successfully processed.

Order Details:
- Order Date: {order.order_date.strftime('%Y-%m-%d %H:%M')}
- Total Amount: HK${order.total_amount}
- Payment Method: {payment_method}
- Shipping Address: {order.shipping_address}

You can view your order details here: {settings.SITE_URL}{reverse('orders:order_detail', args=[order.id])}

Best regards,
Your Company
"""
    notification = EmailNotification.objects.create(
        order=order,
        notification_type='PAYMENT_SUCCESS',
        recipient_email=order.receipient_email if hasattr(order, 'receipient_email') else order.userId.email,
        subject=subject,
        message=message
    )
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [notification.recipient_email],
            fail_silently=False,
        )
        notification.is_sent = True
    except Exception as e:
        notification.error_message = str(e)
    notification.save()

def send_payment_failed_email(order, reason='Payment was cancelled or failed'):
    subject = f'Payment Failed - Order #{order.id}'
    message = f"""
Dear {order.receipient},

We’re sorry, but there was an issue processing your payment for Order #{order.id}.

Reason: {reason}

Order Details:
- Order Date: {order.order_date.strftime('%Y-%m-%d %H:%M')}
- Total Amount: HK${order.total_amount}

Please try again by visiting: {settings.SITE_URL}{reverse('payments:payment', args=[order.id])}

If you need assistance, contact us at support@yourcompany.com.

Best regards,
Your Company
"""
    notification = EmailNotification.objects.create(
        order=order,
        notification_type='PAYMENT_FAILED',
        recipient_email=order.receipient_email if hasattr(order, 'receipient_email') else order.userId.email,
        subject=subject,
        message=message
    )
    
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [notification.recipient_email],
            fail_silently=False,
        )
        notification.is_sent = True
    except Exception as e:
        notification.error_message = str(e)
    notification.save()
