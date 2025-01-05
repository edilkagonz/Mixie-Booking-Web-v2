from django.db import models
from cryptography.fernet import Fernet
import base64
import os

# Generate a key (only run this once and store it securely)
KEY = Fernet.generate_key()

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Package(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Package name
    description = models.TextField(blank=True)           # Package description
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price
    duration = models.CharField(max_length=50)           # Duration (e.g., '1 Hour')
    is_active = models.BooleanField(default=True)        # Enable/Disable package

    def __str__(self):
        return f"{self.name} (${self.price})"
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('refunded', 'Refunded'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    date = models.DateField()
    time = models.TimeField(default='10:00:00')
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    deposit_paid = models.BooleanField(default=False)  # Tracks deposit payment
    balance_paid = models.BooleanField(default=False)  # Tracks remaining balance payment
    created_at = models.DateTimeField(auto_now_add=True)
    consent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.date} - {self.package.name}"




class DisabledDate(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)
    
class DataRequest(models.Model):
    REQUEST_TYPES = [
        ('access', 'Data Access'),
        ('deletion', 'Data Deletion'),
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)
    reason = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.request_type}"



