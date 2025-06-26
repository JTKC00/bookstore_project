# notification/utils.py
from django.core.mail import send_mail
from django.conf import settings
from .models import EmailNotification
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def send_payment_success_email(order, payment_method):
    # 使用 userId.email 作為收件人郵箱
    recipient_email = getattr(order.userId, 'email', None)
    if not recipient_email:
        logger.error(f"No email found for order {order.id}, user {order.userId}")
        return

    subject = f'付款確認 - 訂單 #{order.id}'
    
    # 生成訂單詳情 URL（使用相對路徑，避免 SITE_URL 問題）
    try:
        order_detail_url = reverse('orders:order_detail', args=[order.id])
    except:
        order_detail_url = f'/orders/detail/{order.id}/'
    
    message = f"""親愛的 {order.receipient}，

感謝您的付款！您的訂單 #{order.id} 已成功處理。

訂單詳情：
- 下單日期：{order.order_date.strftime('%Y年%m月%d日 %H:%M')}
- 總金額：HK${order.total_amount}
- 付款方式：{payment_method}
- 配送地址：{order.shipping_address}
- 收件人電話：{order.receipient_phone}

您可以在此查看訂單詳情：http://localhost:8000{order_detail_url}

謝謝！
開心書店
"""
    
    print(f"[DEBUG] 準備發送付款成功郵件給 {recipient_email}")
    print(f"[DEBUG] 郵件主題: {subject}")
    
    notification = EmailNotification.objects.create(
        order=order,
        notification_type='PAYMENT_SUCCESS',
        recipient_email=recipient_email,
        subject=subject,
        message=message
    )
    
    try:
        # 檢查郵件設置
        if not hasattr(settings, 'DEFAULT_FROM_EMAIL') or not settings.DEFAULT_FROM_EMAIL:
            print(f"[DEBUG] DEFAULT_FROM_EMAIL 未設置，使用預設值")
            from_email = 'noreply@bookstore.com'
        else:
            from_email = settings.DEFAULT_FROM_EMAIL
            
        print(f"[DEBUG] 從 {from_email} 發送郵件到 {recipient_email}")
        
        send_mail(
            subject,
            message,
            from_email,
            [recipient_email],
            fail_silently=False,
        )
        notification.is_sent = True
        print(f"[DEBUG] 郵件發送成功")
    except Exception as e:
        notification.error_message = str(e)
        logger.error(f"Failed to send payment success email for order {order.id}: {str(e)}")
        print(f"[DEBUG] 郵件發送失敗: {str(e)}")
    
    notification.save()

def send_payment_failed_email(order, reason='Payment was cancelled or failed'):
    recipient_email = getattr(order.userId, 'email', None)
    if not recipient_email:
        logger.error(f"No email found for order {order.id}, user {order.userId}")
        return

    subject = f'Payment Failed - Order #{order.id}'
    message = f"""
Dear {order.receipient},

We’re sorry, but there was an issue processing your payment for Order #{order.id}.

Reason: {reason}

Order Details:
- Order Date: {order.order_date.strftime('%Y-%m-%d %H:%M')}
- Total Amount: HK${order.total_amount}
- Shipping Address: {order.shipping_address}
- Recipient Phone: {order.receipient_phone}

Please try again by visiting: {settings.SITE_URL}{reverse('payments:payment', args=[order.id])}

If you need assistance, contact us at support@yourcompany.com.

Best regards,
Your Company
"""
    notification = EmailNotification.objects.create(
        order=order,
        notification_type='PAYMENT_FAILED',
        recipient_email=recipient_email,
        subject=subject,
        message=message
    )
    
    try:
        # 檢查郵件設置
        if not hasattr(settings, 'DEFAULT_FROM_EMAIL') or not settings.DEFAULT_FROM_EMAIL:
            from_email = 'noreply@bookstore.com'
        else:
            from_email = settings.DEFAULT_FROM_EMAIL
            
        send_mail(
            subject,
            message,
            from_email,
            [recipient_email],
            fail_silently=False,
        )
        notification.is_sent = True
        print(f"[DEBUG] 付款失敗郵件發送成功到 {recipient_email}")
    except Exception as e:
        notification.error_message = str(e)
        logger.error(f"Failed to send payment failed email for order {order.id}: {str(e)}")
        print(f"[DEBUG] 付款失敗郵件發送失敗: {str(e)}")
    notification.save()