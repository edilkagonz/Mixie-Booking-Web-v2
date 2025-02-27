from django.contrib import admin
from .models import Contact, Booking, DisabledDate, Package
from paypal.standard.ipn.models import PayPalIPN
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
import paypalrestsdk  


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')
    list_filter = ('submitted_at',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    # Add refund-related fields to the display
    list_display = (
        'name', 'email', 'date', 'time', 
        'get_package_name', 'payment_status', 
        'transaction_id', 'deposit_paid', 'balance_paid', 
        'refund_amount', 'refund_transaction_id', 'refund_date'
    )
    search_fields = ('name', 'email')
    list_filter = ('date', 'payment_status', 'refund_date')
    actions = ['generate_payment_link', 'mark_balance_paid', 'mark_refunded', 'issue_refund']

    def get_package_name(self, obj):
        return obj.package.name  # Show package name
    get_package_name.short_description = 'Package'

    # Action to generate PayPal payment link
    def generate_payment_link(self, request, queryset):
        """
        Generate PayPal payment link for remaining balance.
        """
        for booking in queryset:
            if not booking.balance_paid and booking.deposit_paid:
                remaining_amount = booking.package.price - Decimal('50.00')
                paypal_dict = {
                    "business": "sb-un0zt35508323@business.example.com",
                    "amount": remaining_amount,
                    "item_name": f"Remaining balance for {booking.package.name} - {booking.name}",
                    "invoice": str(booking.id),
                    "notify_url": "https://your-ngrok-url/paypal/",
                    "return": "https://your-ngrok-url/payment/success/",
                    "cancel_return": "https://your-ngrok-url/payment/cancel/",
                    "currency_code": "USD",
                    "cmd": "_xclick",
                }

                # Properly construct the PayPal URL
                payment_link = (
                    "https://www.sandbox.paypal.com/cgi-bin/webscr?"
                    + "&".join(f"{key}={value}" for key, value in paypal_dict.items())
                )

                self.message_user(request, f"Payment link for Booking {booking.id}: {payment_link}")
            else:
                self.message_user(request, f"Booking {booking.id} already has balance paid or deposit not paid.")
    generate_payment_link.short_description = "Generate Payment Link for Remaining Balance"


    # Action to manually mark balance as paid
    def mark_balance_paid(self, request, queryset):
        """
        Mark remaining balance as paid manually.
        """
        for booking in queryset:
            if not booking.balance_paid and booking.deposit_paid:
                booking.balance_paid = True
                booking.payment_status = 'confirmed'
                booking.save()
                self.message_user(request, f"Booking {booking.id} marked as balance paid.")
            else:
                self.message_user(request, f"Booking {booking.id} already has balance paid or deposit not paid.")
    mark_balance_paid.short_description = "Manually Mark Balance as Paid"

    # Manual Refund Action - Status Only
    def mark_refunded(self, request, queryset):
        """
        Manually mark a booking as refunded without processing payment.
        """
        for booking in queryset:
            if booking.payment_status == 'confirmed':  # Only confirmed bookings
                booking.payment_status = 'refunded'
                booking.save()
                self.message_user(request, f"Booking {booking.id} marked as refunded.")
            else:
                self.message_user(request, f"Booking {booking.id} cannot be refunded (not confirmed).")
    mark_refunded.short_description = "Mark as Refunded (Manual)"

    # Automated Refund Processing via PayPal
    def issue_refund(self, request, queryset):
        """
        Attempt to process a PayPal refund and update the status.
        """
        for booking in queryset:
            if booking.payment_status == 'confirmed' and booking.transaction_id:
                try:
                    # Process refund via PayPal SDK
                    payment = paypalrestsdk.Payment.find(booking.transaction_id)
                    refund = payment.refund({
                        "amount": {
                            "total": str(booking.package.price),  # Refund full price
                            "currency": "USD"
                        }
                    })

                    if refund.success():
                        booking.payment_status = 'refunded'
                        booking.refund_amount = booking.package.price
                        booking.refund_transaction_id = refund.id
                        booking.refund_date = date.today()
                        booking.save()
                        self.message_user(request, f"Refund successful for Booking {booking.id}.")
                    else:
                        self.message_user(request, f"Refund failed for Booking {booking.id}. Error: {refund.error}")

                except Exception as e:
                    self.message_user(request, f"Refund failed for Booking {booking.id}. Error: {str(e)}")
            else:
                self.message_user(request, f"Booking {booking.id} cannot be refunded (invalid status or transaction ID).")
    issue_refund.short_description = "Process Refund via PayPal"




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
