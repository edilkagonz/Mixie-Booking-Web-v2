from django.core.management.base import BaseCommand
from bookings.models import Booking
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from datetime import date, timedelta
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process remaining balance payments for bookings due tomorrow'

    def handle(self, *args, **kwargs):
        try:
            # Find bookings for tomorrow where deposit is paid but balance is not
            tomorrow = date.today() + timedelta(days=1)
            bookings = Booking.objects.filter(date=tomorrow, deposit_paid=True, balance_paid=False)

            for booking in bookings:
                # Calculate remaining balance
                remaining_amount = booking.package.price - Decimal('50.00')  # Deduct deposit amount
                
                # Generate PayPal payment form data
                paypal_dict = {
                    "business": "sb-un0zt35508323@business.example.com",
                    "amount": remaining_amount,
                    "item_name": f"Remaining balance for {booking.package.name} - {booking.name}",
                    "invoice": str(booking.id),
                    "notify_url": "https://21b9-97-101-224-173.ngrok-free.app/paypal/",
                    "return_url": "https://21b9-97-101-224-173.ngrok-free.app/payment/success/",
                    "cancel_return": "https://21b9-97-101-224-173.ngrok-free.app/payment/cancel/",
                    "currency_code": "USD",
                }

                # Log the generated payment form data
                logger.info(f"Generated PayPal payment for booking {booking.id}: {paypal_dict}")

            self.stdout.write(self.style.SUCCESS("Successfully processed remaining balances for bookings tomorrow."))
        except Exception as e:
            logger.error(f"Error processing remaining payments: {str(e)}")
            self.stderr.write(self.style.ERROR("Error processing payments. Check logs for details."))
