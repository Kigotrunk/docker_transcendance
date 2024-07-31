from django.db import models
from myaccount.models import Account
from django.conf import settings
from django.utils import timezone

# Create your models here.

class Conversation(models.Model):
    user1 = models.ForeignKey(Account, related_name='conversations_as_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(Account, related_name='conversations_as_user2', on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    last_message_sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-last_message_sent_at', '-time']

    def __str__(self):
        return f"Conversation between {self.user1.username} and {self.user2.username}"

class PrivateMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    message = models.CharField()
    issuer = models.ForeignKey(Account, related_name='messages_issuer', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, related_name='messages_receiver', on_delete=models.CASCADE)
    moment = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-moment']

    def __str__(self):
        
        return f"{self.issuer} send message"
    

    

class UserBlock(models.Model):
    blocker = models.ForeignKey(Account, related_name='blocking', on_delete=models.CASCADE)
    blocked = models.ForeignKey(Account, related_name='blocked_by', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocker} blocked {self.blocked}"
