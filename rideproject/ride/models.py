from django.db import models
from accounts.models import Account

class Ride(models.Model):
    rider = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='rides_as_rider')
    driver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='rides_as_driver')
    pickup_location = models.CharField(max_length=100)
    dropoff_location = models.CharField(max_length=100)
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('started', 'Started'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
