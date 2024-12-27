from django.contrib import admin
from django.urls import path, include 
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.ipn import urls as paypal_urls 
from . import views  


urlpatterns = [
    # Admin portal
    path('admin/', admin.site.urls),

    # Home page (default route)
    path('', views.home, name='home'),

    # Booking form URLs
    path('book/', include('bookings.urls')),

    # PayPal IPN URL
    path('paypal/', include(paypal_urls)),

]

# --- Logging Setup ---
import logging

# Create a logger
logger = logging.getLogger(__name__)

# Set the logging level
logger.setLevel(logging.DEBUG)

# Create a file handler
file_handler = logging.FileHandler('mixie_booking.log')
file_handler.setLevel(logging.DEBUG)

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter and set it for the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
