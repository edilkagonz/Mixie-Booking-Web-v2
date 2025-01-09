from django.core.management.base import BaseCommand
from bookings.models import Booking
from paypal.standard.forms import PayPalPaymentsForm
from django.urls import reverse
from datetime import date
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Process remaining payments for bookings due today'

    def handle(self, *args, **kwargs):
        try:
            # Find bookings due today with deposits paid and balances not paid
            bookings = Booking.objects.filter(date=date.today(), deposit_paid=True, balance_paid=False)

            for booking in bookings:
                # Calculate the remaining balance
                remaining_amount = booking.package.price - Decimal('50.00')

                # Prepare PayPal payment details
                paypal_dict = {
                    "business": "sb-un0zt35508323@business.example.com",
                    "amount": remaining_amount,
                    "item_name": f"Remaining balance for {booking.package.name} - {booking.name}",
                    "invoice": f"{booking.id}-balance",  # Create a unique invoice for the balance
                    "notify_url": "https://47c5-97-101-224-173.ngrok-free.app/paypal/",  # IPN endpoint
                    "return_url": "https://47c5-97-101-224-173.ngrok-free.app/payment/success/",
                    "cancel_return": "https://47c5-97-101-224-173.ngrok-free.app/payment/cancel/",
                    "currency_code": "USD",
                }

                # Generate the PayPal form
                form = PayPalPaymentsForm(initial=paypal_dict)

                # Log the payment attempt
                logger.info(f"Processing remaining payment for booking {booking.id}. Amount: ${remaining_amount}")

                # Instead of directly marking the balance_paid, let IPN handle it after PayPal processes the payment.

            self.stdout.write(self.style.SUCCESS('Successfully sent remaining balance forms for processing.'))

        except Exception as e:
            logger.error(f"Error processing payments: {str(e)}")
            self.stderr.write(self.style.ERROR('Error processing payments. Check logs for details.'))
