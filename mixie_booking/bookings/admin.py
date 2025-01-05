from django.contrib import admin
from .models import Contact, Booking, DisabledDate, Package
from paypal.standard.ipn.models import PayPalIPN
import paypalrestsdk  


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'time', 'get_package_name', 'payment_status', 'transaction_id')
    search_fields = ('name', 'email')
    list_filter = ('date', 'payment_status')

    def get_package_name(self, obj):
        return obj.package.name  # Show package name
    get_package_name.short_description = 'Package'

    actions = ['mark_refunded']

    # Refund Action (Manual Status Update)
    def mark_refunded(self, request, queryset):
        for booking in queryset:
            if booking.payment_status == 'confirmed':
                booking.payment_status = 'refunded'
                booking.save()
                self.message_user(request, f"Booking {booking.id} marked as refunded.")
            else:
                self.message_user(request, f"Booking {booking.id} cannot be refunded (not confirmed).")
    mark_refunded.short_description = "Mark as Refunded"


# Define a custom admin mixin for common functionality
class CustomAdminMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

@admin.register(DisabledDate)
class DisabledDateAdmin(admin.ModelAdmin):
    list_display = ('date',)

from .models import Package

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_active')  # Display fields
    list_editable = ('price', 'duration', 'is_active')  # Allow quick editing
    search_fields = ('name',)
    list_filter = ('is_active',)
