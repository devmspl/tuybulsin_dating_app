from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from personalprofile.models import PersonalInformation
from user_management.models import CustomUser 

class LikeDislike(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    profile = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'profile')

    def __str__(self):
        return str(f"this user {self.user.id} like this profile {self.profile.user.id}")