from django.shortcuts import render, redirect
from django.contrib import messages
from bookings.forms import BookingForm
from bookings.forms import ContactForm 

def home(request):
    return render(request, 'index.html')  # Points to templates/index.html

def contact_submit(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('/')  # Redirect to home page after success
        else:
            messages.error(request, 'There was an error sending your message.')
    else:
        form = ContactForm()

    # Render back to the index page with the form
    return render(request, 'index.html', {'form': form})


