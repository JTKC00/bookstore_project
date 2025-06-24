from django.contrib import admin
from .models import EmailNotification

@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'notification_type', 'recipient_email', 'subject', 'is_sent', 'sent_at']
    list_filter = ['notification_type', 'is_sent', 'sent_at']
    search_fields = ['recipient_email', 'subject', 'order__id']
    readonly_fields = ['sent_at', 'message', 'error_message']
    date_hierarchy = 'sent_at'

    def order_id(self, obj):
        return obj.order.id
    order_id.short_description = 'Order ID'
    order_id.admin_order_field = 'order__id'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('order')