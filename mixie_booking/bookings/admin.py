from django.contrib import admin
from .models import Contact, Booking, DisabledDate

from paypal.standard.ipn.models import PayPalIPN  


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'time', 'package', 'payment_status', 'transaction_id')
    search_fields = ('name', 'email')
    list_filter = ('date', 'payment_status')
    actions = ['refund_booking']

    def refund_booking(self, request, queryset):
        for booking in queryset:
            # Update status to refunded
            booking.payment_status = 'refunded'
            booking.save()
            self.message_user(request, f"Refund initiated for {booking.name}.")
    refund_booking.short_description = "Refund selected bookings"

@admin.register(DisabledDate)
class DisabledDateAdmin(admin.ModelAdmin):
    list_display = ('date',)
