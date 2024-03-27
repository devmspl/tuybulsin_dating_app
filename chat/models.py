from django.conf import settings
from django.db import models

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name='message_sender',default=None)
    message = models.CharField(max_length=2000, blank=True,null=True)
    attachment = models.FileField(blank=True)
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver',default=None)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-timestamp',)

    def __str__(self):
        return f"From {self.sender} to {self.recipient}: {self.message}"