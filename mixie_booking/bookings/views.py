import logging
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import BookingForm
from .forms import ContactForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from .models import Booking, DisabledDate
from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from django.core.mail import send_mail
from django.urls import reverse
from datetime import date, timedelta

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
    selected_package = request.GET.get('package', '')
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            # Check if the selected date is disabled
            if DisabledDate.objects.filter(date=booking.date).exists():
                messages.error(request, "The selected date is not available.")
                return redirect('book_now')

            booking.payment_status = 'pending'
            booking.save()

            # Prepare PayPal form
            paypal_dict = {
                "business": "sb-un0zt35508323@business.example.com",  
                "amount": "50.00",  # Fixed deposit amount
                "item_name": f"Booking Deposit for {booking.name}",
                "invoice": str(booking.id),
                "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
                "return_url": request.build_absolute_uri(reverse('payment_success')),
                "cancel_return": request.build_absolute_uri(reverse('payment_cancel')),
            }


            form = PayPalPaymentsForm(initial=paypal_dict)
            return render(request, "booking_payment.html", {'form': form, 'booking': booking})
    else:
        form = BookingForm(initial={'package': selected_package})
    return render(request, 'booking.html', {'form': form})


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
    logger.info(f"IPN received: {ipn_obj}")  # Debug incoming IPN data

    try:
        # Log entire IPN object
        logger.debug(f"IPN Data: {ipn_obj}")

        # Match IPN invoice with Booking ID
        invoice_id = ipn_obj.invoice  # Get invoice
        booking = Booking.objects.get(id=invoice_id)  # Match Booking by ID

        # Check if payment status is "Completed"
        if ipn_obj.payment_status == "Completed":
            booking.payment_status = 'confirmed'
            booking.transaction_id = ipn_obj.txn_id
            booking.save()

            # Add date to disabled dates
            DisabledDate.objects.get_or_create(date=booking.date)

            logger.info(f"Booking {invoice_id} updated to confirmed.")
        
        # Handle refunds
        elif ipn_obj.payment_status == "Refunded":
            booking.payment_status = 'refunded'
            booking.save()
            logger.info(f"Booking {invoice_id} updated to refunded.")
        else:
            logger.warning(f"Unhandled payment status: {ipn_obj.payment_status}")
    except Booking.DoesNotExist:
        logger.error(f"Booking with ID {invoice_id} not found.")
    except Exception as e:
        logger.error(f"Error processing IPN: {str(e)}")



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

