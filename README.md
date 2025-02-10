# Mixie The Clown - Booking Platform 🎪✨

Overview

This is a Django-based web platform designed to streamline booking and payment processing for Mixie The Clown’s entertainment services. The system allows customers to browse available services, schedule events, and make payments via PayPal IPN while providing an admin panel for managing bookings and availability.

Features

✅ User-Friendly Booking – Customers can book services without account creation.
✅ Real-Time Calendar – Displays available dates for scheduling.
✅ Secure Payment Processing – Integrated PayPal IPN for deposit payments.
✅ Admin Dashboard – Manage bookings, update availability, and process cancellations.
✅ Refund Handling – Cancellation requests are reviewed by the admin, and refunds are processed manually in PayPal.
✅ Mobile-Friendly & Responsive – Optimized for all devices.

Tech Stack
	•	Backend: Python (Django)
	•	Frontend: HTML, CSS, JavaScript
	•	Database: MySQL
	•	Payments: PayPal IPN Integration

Installation & Setup
	1.	Clone the Repository:

git clone https://github.com/your-username/mixie-booking.git
cd mixie-booking


	2.	Create Virtual Environment & Install Dependencies:

python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
pip install -r requirements.txt


	3.	Apply Migrations & Start Server:

python manage.py migrate
python manage.py runserver


	4.	Access the Website:
Open http://127.0.0.1:8000 in your browser.

Admin Access

To access the Django Admin Panel for managing bookings:
	1.	Create a superuser:

python manage.py createsuperuser


	2.	Login at: http://127.0.0.1:8000/admin

How PayPal IPN Works in This Project
	•	Users pay a deposit via PayPal.
	•	PayPal sends an IPN notification to the backend confirming payment.
	•	The system updates the booking status to “Confirmed.”
	•	Admin manually processes refunds if needed via PayPal.


🚀 Happy Booking! 🎈
