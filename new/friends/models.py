from django.db import models
from django.http import HttpResponse

from myaccount.models import Account

# Create your models here.

from django.db import models
from myaccount.models import Account

class Friend(models.Model):
    user = models.ForeignKey(Account, related_name='friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(Account, related_name='friend_of', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} is friends with {self.friend}"

class Invitation(models.Model):
    WAITING = 'Waiting'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (WAITING, 'Waiting'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    ]

    sender = models.ForeignKey(Account, related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, related_name='receiver', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=WAITING)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"Invitation from {self.sender} to {self.receiver} ({self.status})"





