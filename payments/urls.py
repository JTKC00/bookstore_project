from django.urls import path
from . import views
from django.views.generic import TemplateView
app_name = 'payments'

urlpatterns = [
    path('payment/<int:order_id>/', views.PaymentPageView.as_view(), name='payment'),
    path('create-checkout-session/<int:order_id>/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('stripe-webhook/', views.stripe_webhook, name='stripe_webhook'),
    path('fps/', views.fps_payment, name='fps_payment'),
    path('paypal/', views.paypal_payment, name='paypal_payment'),
    path('success/', TemplateView.as_view(template_name='payments/success.html'), name='success'),
    path('cancel/', TemplateView.as_view(template_name='payments/cancel.html'), name='cancel'),
]