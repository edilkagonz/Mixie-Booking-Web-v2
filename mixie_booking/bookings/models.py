from django.db import models


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
    
class Booking(models.Model):
    PACKAGE_CHOICES = [
        ('basic', 'Basic Fun ($199)'),
        ('premium', 'Premium Magic ($299)'),
        ('deluxe', 'Deluxe Party ($399)'),
    ]

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
    time = models.TimeField(default='10:00:00')  # Default time
    package = models.CharField(max_length=50, choices=PACKAGE_CHOICES)
    message = models.TextField(blank=True)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date} - {self.package}"


class DisabledDate(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return str(self.date)