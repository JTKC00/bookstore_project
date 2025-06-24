from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('payment/<int:order_id>/', views.PaymentPageView.as_view(), name='payment'),
    path('create-checkout-session/<int:order_id>/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('fps/<int:order_id>/', views.fps_payment, name='fps_payment'),
    path('success/', views.payment_success, name='success'),
    path('cancel/', views.payment_cancel, name='cancel'),
]