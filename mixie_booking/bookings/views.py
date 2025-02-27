import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import BookingForm
from .forms import ContactForm, DataRequestForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from .models import Booking, DisabledDate, Package
from paypal.standard.ipn.signals import valid_ipn_received
from paypal.standard.models import ST_PP_COMPLETED
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from datetime import date, timedelta
from paypalrestsdk import Payment

def contact_submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save data to the database
            return JsonResponse({'success': True})  # Send JSON success response
        else:
            return JsonResponse({'success': False, 'errors': form.errors})  # Send errors as JSON
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request.'})
    
def book_now(request):
    package_id = request.GET.get('package', None)
    selected_package = None

    # Validate selected package
    if package_id:
        try:
            selected_package = Package.objects.get(id=package_id, is_active=True)
        except Package.DoesNotExist:
            selected_package = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Save booking with 'pending' status
            booking = form.save(commit=False)
            booking.payment_status = 'pending'
            booking.save()

            # Redirect to payment page with booking ID
            return redirect('booking_payment', booking_id=booking.id)
    else:
        form = BookingForm(selected_package=selected_package)

    return render(request, 'booking.html', {
        'form': form,
        'selected_package': selected_package
    })



@csrf_exempt
def payment_success(request):
    messages.success(request, "Payment successful! Your booking is confirmed.")
    return redirect('home')


@csrf_exempt
def payment_cancel(request):
    messages.error(request, "Payment canceled. Your booking is not confirmed.")
    return redirect('home')


logger = logging.getLogger(__name__)

@receiver(valid_ipn_received)
def paypal_ipn_handler(sender, **kwargs):
    ipn_obj = sender

    logger.debug(f"IPN Raw Data: {ipn_obj}")
   # logger.info(f"IPN Received: {ipn_obj}")

    try:
        # Check booking by invoice ID
        booking = Booking.objects.get(id=int(ipn_obj.invoice))

        # Validate the IPN response
        if (
            ipn_obj.payment_status == "Completed" and  # Payment completed
            ipn_obj.receiver_email == "sb-un0zt35508323@business.example.com" and  # Sandbox email
            ipn_obj.mc_currency == "USD"  # Ensure currency is correct
        ):
            if float(ipn_obj.mc_gross) == 50.00:  # Deposit amount
                # Mark deposit as paid
                booking.payment_status = 'confirmed'
                booking.transaction_id = ipn_obj.txn_id
                booking.deposit_paid = True
                booking.save()

                # Disable selected date
                DisabledDate.objects.get_or_create(date=booking.date)
                logger.info(f"Deposit paid for booking {booking.id}. Date disabled.")
                
                send_booking_confirmation(
                    email=booking.email,  # Replace with actual email field from the booking
                    subject="Booking Confirmation",
                    message=f"Dear {booking.name},\n\n"
                            f"Your booking for {booking.package.name} on {booking.date} has been confirmed.\n"
                            f"Transaction ID: {booking.transaction_id}\n\n"
                            f"Thank you!"
                )
                logger.info(f"Booking confirmation email sent to {booking.email}.")

            elif float(ipn_obj.mc_gross) == float(booking.package.price - 50.00):  # Remaining balance
                # Mark remaining balance as paid
                booking.balance_paid = True
                booking.payment_status = 'confirmed'
                booking.transaction_id = ipn_obj.txn_id
                booking.save()

                logger.info(f"Remaining balance paid for booking {booking.id}.")
            else:
                logger.warning(f"IPN amount mismatch for booking {booking.id}. Expected: Deposit or Remaining Balance, Got: {ipn_obj.mc_gross}")

        elif ipn_obj.payment_status == "Refunded":
            # Handle refunds
            refunded_amount = float(ipn_obj.mc_gross)  # Refund amount
            if booking.refund_amount:  # Partial refunds
                booking.refund_amount += refunded_amount
            else:
                booking.refund_amount = refunded_amount

            # Update refund details
            booking.refund_transaction_id = ipn_obj.parent_txn_id
            booking.refund_date = ipn_obj.payment_date
            booking.payment_status = 'refunded'
            booking.save()
            logger.info(f"Booking {booking.id} refunded. Amount: {booking.refund_amount}, Transaction ID: {booking.refund_transaction_id}")

            # Release the associated date
            DisabledDate.objects.filter(date=booking.date).delete()

        else:
            logger.warning(f"Unhandled status for booking {booking.id}: {ipn_obj.payment_status}")

    except Booking.DoesNotExist:
        logger.error(f"Booking not found for invoice {ipn_obj.invoice}")
    except Exception as e:
        logger.error(f"Error processing IPN for booking: {str(e)}")


logger = logging.getLogger(__name__)

# import paypalrestsdk



def get_disabled_dates(request):
    # Fetch disabled dates from the database
    disabled_dates = list(DisabledDate.objects.values_list('date', flat=True))
    today = date.today()
    # Add the next 3 days to the disabled dates
    for i in range(3):
        disabled_dates.append(today + timedelta(days=i))

    # Format dates to match JavaScript date format
    disabled_dates = [d.strftime('%Y-%m-%d') for d in disabled_dates]
    return JsonResponse({'disabled_dates': disabled_dates})

def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def data_request_view(request):
    if request.method == 'POST':
        form = DataRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your request has been submitted. We will get back to you soon.")
            return redirect('home')  # Replace 'home' with the appropriate route
        else:
            messages.error(request, "There was an error submitting your request.")
    else:
        form = DataRequestForm()

    return render(request, 'data_request.html', {'form': form})

def home(request):
    # Fetch all active packages
    packages = Package.objects.filter(is_active=True)
    return render(request, 'index.html', {'packages': packages})

def booking_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Set deposit amount to $50
    deposit_amount = 50.00

    paypal_dict = {
        "business": "sb-un0zt35508323@business.example.com",
        "amount": deposit_amount,  # Charge deposit amount
        "item_name": f"Deposit for {booking.package.name} - {booking.name}",
        "invoice": str(booking.id),  # Unique booking ID
        "notify_url":"https://8f52-97-101-224-173.ngrok-free.app/paypal/",
        "return_url": request.build_absolute_uri(reverse('payment_success')),
        "cancel_return": request.build_absolute_uri(reverse('payment_cancel')),
        "currency_code": "USD",
    }

    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'booking_payment.html', {'form': form, 'booking': booking})

logger = logging.getLogger(__name__)

def send_booking_confirmation(email, subject, message):
    """
    Send a booking confirmation email and log the result.
    """
    try:
        send_mail(subject, message, 'your-email@example.com', [email])
        logger.info(f"Email sent successfully to {email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        return False


