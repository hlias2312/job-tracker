from django.db import models
from django.contrib.auth.models import User

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interview', 'Interview'),
        ('offer', 'Offer'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    date_applied = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.position} at {self.company}"